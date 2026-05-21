from django.conf import settings
from django.db import models
from django.utils import timezone


class CourseType(models.Model):
    """
    General type/category of course.

    Examples:
    - Individual Classes
    - Company English Training
    - FCE Preparation
    - Conversation Course
    """

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    is_for_companies = models.BooleanField(default=False)
    is_for_individual = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Specific course instance.

    Examples:
    - Individual Classes.01
    - Individual Classes.02
    - Company English - ACME 2026
    - FCE B2 Group.01
    """

    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    name = models.CharField(max_length=200)

    company = models.ForeignKey(
        "profiles.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        help_text="Only needed for company courses."
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_taught"
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name



class CourseEnrollment(models.Model):
    """
    Connects a user/student/worker to a specific course.
    - One course can have many students.
    - One student can be enrolled in many courses.
    - Each enrolment can store its own status/objective.
    """

    ENROLLMENT_STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default="active"
    )

    target_level = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional target CEFR level, e.g. B2, C1."
    )

    learning_objective = models.TextField(
        blank=True,
        help_text="Optional individual or company learning objective."
    )

    class Meta:
        unique_together = ("course", "student")
        ordering = ["course", "student"]

    def __str__(self):
        return f"{self.student} - {self.course}"

    @property
    def total_assigned_classes(self):
        return self.course.class_sessions.filter(
            is_cancelled=False
        ).count()
    
    # Do not store attendance percentage in the database.
    # Calculate it from Attendance through properties:
    @property
    def classes_attended(self):
        return Attendance.objects.filter(
            class_session__course=self.course,
            class_session__is_cancelled=False,
            student=self.student,
            status="attended"
        ).count()

    @property
    def classes_missed(self):
        return Attendance.objects.filter(
            class_session__course=self.course,
            class_session__is_cancelled=False,
            student=self.student,
            status="missed"
        ).count()

    @property
    def attendance_percentage(self):
        total = self.total_assigned_classes

        if total == 0:
            return 0

        return round((self.classes_attended / total) * 100)

    @property
    def has_low_attendance_warning(self):
        total = self.total_assigned_classes

        if total < 3:
            return False

        return self.attendance_percentage < 75


class ClassSession(models.Model):
    """
    One scheduled lesson for a specific course.
    E.g.: Individual Classes.01
    Class 1
    Class 2
    Class 3
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="class_sessions"
    )

    title = models.CharField(
        max_length=200,
        default="English Class"
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    meeting_link = models.URLField(blank=True)

    topic = models.CharField(max_length=200, blank=True)

    is_cancelled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.course} - {self.start_time:%d/%m/%Y %H:%M}"

    @property
    def is_past(self):
        return self.end_time < timezone.now()



class Attendance(models.Model):
    '''
    In a group/company course, many students attend
    the same class session, but each has 
    their own attendance status.
    Supports:
    - 1-to-1 individual classes
    - group company classes

    '''
    ATTENDANCE_STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("attended", "Attended"),
        ("missed", "Missed"),
        ("excused", "Excused"),
        ("cancelled", "Cancelled"),
    ]

    class_session = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUS_CHOICES,
        default="scheduled"
    )

    minutes_late = models.PositiveIntegerField(
        default=0,
        help_text="Number of minutes late. Use 0 if on time."
    )

    notes = models.TextField(blank=True)

    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("class_session", "student")
        ordering = ["class_session__start_time", "student"]

    def __str__(self):
        return f"{self.student} - {self.class_session} - {self.status}"

    @property
    def was_punctual(self):
        return self.status == "attended" and self.minutes_late == 0
