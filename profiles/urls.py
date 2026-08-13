from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),
    
    path("profile_settings/", views.profile_settings, name="profile_settings"),


    # STUDENT PAGES    
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/my_course/", views.my_course, name="my_course"),
    path("student/my_calendar/", views.my_calendar, name="my_calendar"),
    path("student/my_calendar/events/", views.my_calendar_events, name="my_calendar_events"),
    path("student/my-learning-progress/", views.my_learning_progress, name="my_learning_progress"),
    path("student/my_attendance/", views.my_attendance, name="my_attendance"),
    path("student/my-skills/", views.my_skills, name="my_skills"),
    path("student/my-learning-progress/assessment/", views.my_learning_progress_assessment, name="my_learning_progress_assessment"),


    # TEACHER PAGES
    path("teacher/teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/teacher_classes_list/", views.teacher_classes_list, name="teacher_classes_list"),
    # Teacher ATTENDANCE: Group Record/ Take/ Update 
    path("teacher/teacher_attendance/", views.teacher_attendance, name="teacher_attendance"),
    path("teacher/attendance/<int:session_id>/take/", views.teacher_take_attendance, name="teacher_take_attendance"),
    path("teacher/attendance/<int:session_id>/detail/", views.teacher_attendance_detail, name="teacher_attendance_detail"),
    # Teacher COURSES
    path("teacher/courses/", views.teacher_courses, name="teacher_courses"),
    # Teacher COURSE DETAILS
    path("teacher/courses/<int:course_id>/", views.teacher_course_details, name="teacher_course_details"),
    path("teacher/courses/<int:course_id>/attendance/", views.teacher_group_attendance, name="teacher_group_attendance"),
    path("teacher/sessions/<int:session_id>/attendance/", views.teacher_session_attendance_detail, name="teacher_session_attendance_detail"),
    path("teacher/courses/<int:course_id>/enrollments/", views.teacher_course_students_list, name="teacher_course_students_list"),
    # Teacher STUDENT DETAILS
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/",views.teacher_student_detail, name="teacher_student_detail"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/update-level/", views.update_student_level, name="update_student_level"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/attendance/", views.student_attendance_record, name="student_attendance_record"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/attendance/<int:attendance_id>/update/", views.update_student_attendance_status, name="update_student_attendance_status"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/academic-profile/", views.student_academic_profile_settings, name="student_academic_profile_settings"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/skills/", views.student_skills_overview, name="student_skills_overview"),
    path("teacher/student-skill/<int:skill_assessment_id>/edit/", views.teacher_edit_student_skill, name="teacher_edit_student_skill"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/assessment_notes", views.teacher_student_assessment_notes, name="teacher_student_assessment_notes"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/progress_chart", views.teacher_student_progress_skills_graph, name="teacher_student_progress_skills_graph"),
    # Teacher RESCHEDULE
    path("teacher/classes/<int:session_id>/pending-reschedule/", views.mark_class_pending_reschedule, name="mark_class_pending_reschedule"),
    path("teacher/reschedule-classes/", views.teacher_reschedule_classes, name="teacher_reschedule_classes"),
    path("teacher/reschedule-classes/<int:session_id>/", views.reschedule_class_detail, name="reschedule_class_detail"),
    # Teacher CALENDAR
    path("teacher/calendar/", views.teacher_calendar, name="teacher_calendar"),
    path("teacher/calendar/events/", views.teacher_calendar_events, name="teacher_calendar_events"),
    # Teacher PROFILE SETTINGS
    path("teacher/teacher_profile_settings/", views.teacher_profile_settings, name="teacher_profile_settings"),


    # COMPANY ADMIN PAGES
    path("company_admin/company_admin_dashboard/", views.company_admin_dashboard, name="company_admin_dashboard"),
    path("company-admin/attendance/", views.company_admin_all_courses_attendance, name="company_admin_all_courses_attendance"),
    path("company-admin/courses/", views.company_admin_courses, name="company_admin_courses"),
    path("company-admin/courses/<int:course_id>/", views.company_admin_course_details, name="company_admin_course_details"),
    path("company-admin/courses/<int:course_id>/attendance/", views.company_admin_course_attendance, name="company_admin_course_attendance"),
    path("company-admin/classes/<int:class_session_id>/attendance/", views.company_admin_course_attendance_detail, name="company_admin_course_attendance_detail"),
    path("company-admin/courses/<int:course_id>/students/", views.company_admin_course_students_list, name="company_admin_course_students_list"),
    path("company-admin/employees/<int:student_id>/", views.company_admin_student_detail, name="company_admin_student_detail"),
    path("company-admin/employees/<int:student_id>/attendance/", views.company_admin_student_attendance_record, name="company_admin_student_attendance_record"),
    path("company-admin/employees/<int:student_id>/skills/", views.company_admin_student_skills_overview, name="company_admin_student_skills_overview"),
    path("company-admin/employees/<int:student_id>/assessment/", views.company_admin_student_teacher_notes, name="company_admin_student_teacher_notes"),
    path("company-admin/employees/<int:student_id>/progress/", views.company_admin_student_progress_skills_graph, name="company_admin_student_progress_skills_graph"),
    path("company-admin/classes/", views.company_admin_classes_list, name="company_admin_classes_list"),
    path("company-admin/employees/", views.company_admin_employees_list, name="company_admin_employees_list"),
    path("company-admin/calendar/", views.company_admin_calendar, name="company_admin_calendar"),
    path("company-admin/calendar/events/", views.company_admin_calendar_events, name="company_admin_calendar_events"),
    path("company_admin/profile_settings/", views.company_admin_profile_settings, name='company_admin_profile_settings'),
    
]

