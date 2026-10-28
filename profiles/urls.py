from django.urls import path

from profiles.views.shared import (
    login_redirect,
    profile,
    profile_settings,
)

from profiles.views.student import (
    student_dashboard,
    my_course,
    my_classes,
    student_mark_class_pending_reschedule,
    my_calendar,
    my_calendar_events,
    my_learning_progress,
    my_attendance,
    my_skills,
    my_learning_progress_assessment,
    my_needs_analysis,
)

from profiles.views.teacher import (
    teacher_dashboard,
    teacher_classes_list,
    teacher_courses,
    teacher_course_details,
    teacher_course_attendance,
    teacher_course_assessment,
    teacher_course_students_list,
    teacher_student_detail,
    teacher_student_term_assessment,
    teacher_term_assessment_detail,
    teacher_create_term_assessment,
    student_academic_profile_settings,
    update_student_level,
    student_attendance_record,
    update_student_attendance_status,
    student_skills_overview,
    teacher_edit_student_skill,
    teacher_student_needs_analysis,
    teacher_student_assessment_notes,
    teacher_calendar,
    teacher_calendar_events,
    teacher_attendance,
    teacher_take_attendance,
    teacher_attendance_detail,
    mark_class_pending_reschedule,
    teacher_reschedule_classes,
    reschedule_class_detail,
    teacher_profile_settings,
)

from profiles.views.company_admin import (
    company_admin_dashboard,
    company_admin_courses,
    company_admin_all_courses_attendance,
    company_admin_course_details,
    company_admin_course_students_list,
    company_admin_course_attendance,
    company_admin_course_attendance_detail,
    company_admin_student_detail,
    company_admin_student_attendance_record,
    company_admin_student_skills_overview,
    company_admin_student_needs_analysis,
    company_admin_student_teacher_notes,
    company_admin_classes_list,
    company_admin_calendar,
    company_admin_calendar_events,
    company_admin_employees_list,
    company_admin_profile_settings,
)

app_name = "profiles"

urlpatterns = [
    path('', profile, name='profile'),
    
    path("profile_settings/", profile_settings, name="profile_settings"),

    # STUDENT PAGES    
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("student/my_course/", my_course, name="my_course"),
    path("student/my_classes/", my_classes, name="my_classes"),
    path("student/classes/<int:session_id>/pending-reschedule/", student_mark_class_pending_reschedule, name="student_mark_class_pending_reschedule"),
    path("student/my_calendar/", my_calendar, name="my_calendar"),
    path("student/my_calendar/events/", my_calendar_events, name="my_calendar_events"),
    path("student/my_learning_progress/", my_learning_progress, name="my_learning_progress"),
    path("student/my_attendance/", my_attendance, name="my_attendance"),
    path("student/my_skills/", my_skills, name="my_skills"),
    path("student/my-learning-needs/", my_needs_analysis, name="my_needs_analysis"),
    path("student/my_learning_progress/assessment/", my_learning_progress_assessment, name="my_learning_progress_assessment"),


    # TEACHER PAGES
    path("teacher/teacher_dashboard/", teacher_dashboard, name="teacher_dashboard"),
    path("teacher/teacher_classes_list/", teacher_classes_list, name="teacher_classes_list"),
    # Teacher ATTENDANCE: Group Record/ Take/ Update 
    path("teacher/teacher_attendance/", teacher_attendance, name="teacher_attendance"),
    path("teacher/attendance/<int:session_id>/take/", teacher_take_attendance, name="teacher_take_attendance"),
    # Teacher COURSES
    path("teacher/courses/", teacher_courses, name="teacher_courses"),
    # Teacher COURSE DETAILS
    path("teacher/courses/<int:course_id>/", teacher_course_details, name="teacher_course_details"),
    path("teacher/courses/<int:course_id>/attendance/", teacher_course_attendance, name="teacher_course_attendance"),
    path("teacher/sessions/<int:session_id>/attendance_detail/", teacher_attendance_detail, name="teacher_attendance_detail"),
    path("teacher/courses/<int:course_id>/enrollments/", teacher_course_students_list, name="teacher_course_students_list"),
    # Teacher STUDENT DETAILS
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/",teacher_student_detail, name="teacher_student_detail"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/update-level/", update_student_level, name="update_student_level"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/attendance/", student_attendance_record, name="student_attendance_record"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/attendance/<int:attendance_id>/update/", update_student_attendance_status, name="update_student_attendance_status"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/academic-profile/", student_academic_profile_settings, name="student_academic_profile_settings"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/skills/", student_skills_overview, name="student_skills_overview"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/assessment/", teacher_student_term_assessment, name="teacher_student_term_assessment"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/assessment/create/", teacher_create_term_assessment, name="teacher_create_term_assessment"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/assessment/<int:assessment_id>/", teacher_term_assessment_detail, name="teacher_term_assessment_detail"),
    path("teacher/course/<int:course_id>/student/<int:enrollment_id>/learning-needs/", teacher_student_needs_analysis, name="teacher_student_needs_analysis"),
    path("teacher/student-skill/<int:skill_assessment_id>/edit/", teacher_edit_student_skill, name="teacher_edit_student_skill"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/assessment_notes", teacher_student_assessment_notes, name="teacher_student_assessment_notes"),
    # Teacher RESCHEDULE
    path("teacher/classes/<int:session_id>/pending-reschedule/", mark_class_pending_reschedule, name="mark_class_pending_reschedule"),
    path("teacher/reschedule-classes/", teacher_reschedule_classes, name="teacher_reschedule_classes"),
    path("teacher/reschedule-classes/<int:session_id>/", reschedule_class_detail, name="reschedule_class_detail"),
    # Teacher CALENDAR
    path("teacher/calendar/", teacher_calendar, name="teacher_calendar"),
    path("teacher/calendar/events/", teacher_calendar_events, name="teacher_calendar_events"),
    # Teacher PROFILE SETTINGS
    path("teacher/teacher_profile_settings/", teacher_profile_settings, name="teacher_profile_settings"),


    # COMPANY ADMIN PAGES
    path("company_admin/company_admin_dashboard/", company_admin_dashboard, name="company_admin_dashboard"),
    path("company-admin/attendance/", company_admin_all_courses_attendance, name="company_admin_all_courses_attendance"),
    path("company-admin/courses/", company_admin_courses, name="company_admin_courses"),
    path("company-admin/courses/<int:course_id>/", company_admin_course_details, name="company_admin_course_details"),
    path("company-admin/courses/<int:course_id>/attendance/", company_admin_course_attendance, name="company_admin_course_attendance"),
    path("company-admin/classes/<int:class_session_id>/attendance/", company_admin_course_attendance_detail, name="company_admin_course_attendance_detail"),
    path("company-admin/courses/<int:course_id>/students/", company_admin_course_students_list, name="company_admin_course_students_list"),
    path("company-admin/employees/<int:student_id>/", company_admin_student_detail, name="company_admin_student_detail"),
    path("company-admin/employees/<int:student_id>/attendance/", company_admin_student_attendance_record, name="company_admin_student_attendance_record"),
    path("company-admin/employees/<int:student_id>/skills/", company_admin_student_skills_overview, name="company_admin_student_skills_overview"),
    path("company-admin/employees/<int:student_id>/assessment/", company_admin_student_teacher_notes, name="company_admin_student_teacher_notes"),
    path("company-admin/student/<int:student_id>/learning-needs/", company_admin_student_needs_analysis, name="company_admin_student_needs_analysis"),    path("company-admin/classes/", company_admin_classes_list, name="company_admin_classes_list"),
    path("company-admin/employees/", company_admin_employees_list, name="company_admin_employees_list"),
    path("company-admin/calendar/", company_admin_calendar, name="company_admin_calendar"),
    path("company-admin/calendar/events/", company_admin_calendar_events, name="company_admin_calendar_events"),
    path("company_admin/profile_settings/", company_admin_profile_settings, name='company_admin_profile_settings'),


    # Teacher COURSE DETAILS - no course yet
    path("teacher/courses/overview/", teacher_course_details, name="teacher_course_details_empty"),
    path("teacher/courses/attendance/", teacher_course_attendance, name="teacher_course_attendance_empty"),
    path("teacher/courses/enrollments/", teacher_course_students_list, name="teacher_course_students_list_empty"),
    path("teacher/courses/assessment/", teacher_course_assessment, name="teacher_course_assessment_empty"),
    path("teacher/courses/<int:course_id>/assessment/", teacher_course_assessment, name="teacher_course_assessment"),
    # Company Admin COURSE DETAILS - no course yet
    path("company-admin/courses/overview/", company_admin_course_details, name="company_admin_course_details_empty"),
    path("company-admin/courses/attendance/", company_admin_course_attendance, name="company_admin_course_attendance_empty"),
    path("company-admin/courses/students/", company_admin_course_students_list, name="company_admin_course_students_list_empty"),

]

