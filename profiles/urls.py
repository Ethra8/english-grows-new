from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),
    # Student pages
    path("profile_settings/", views.profile_settings, name="profile_settings"),    
    path("student/my_course/", views.my_course, name="my_course"),
    path("student/my_attendance/", views.my_attendance, name="my_attendance"),
    path("student/my_calendar/", views.my_calendar, name="my_calendar"),
    path("student/my_calendar/events/", views.my_calendar_events, name="my_calendar_events"),
    # Teacher pages
    path("teacher/teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/teacher_classes_list/", views.teacher_classes_list, name="teacher_classes_list"),
    
    path("teacher/teacher_attendance/", views.teacher_attendance, name="teacher_attendance"),
    path("teacher/attendance/<int:session_id>/take/", views.teacher_take_attendance, name="teacher_take_attendance"),
    path("teacher/attendance/<int:session_id>/detail/", views.teacher_attendance_detail, name="teacher_attendance_detail"),
    
    path("teacher/courses/", views.teacher_courses, name="teacher_courses"),
    path("teacher/courses/<int:course_id>/", views.teacher_course_details, name="teacher_course_details"),
    path("teacher/courses/<int:course_id>/attendance/", views.teacher_group_attendance, name="teacher_group_attendance"),
    path("teacher/sessions/<int:session_id>/attendance/", views.teacher_session_attendance_detail, name="teacher_session_attendance_detail"),
    path("teacher/courses/<int:course_id>/enrollments/", views.teacher_course_students_list, name="teacher_course_students_list"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/",views.teacher_student_detail, name="teacher_student_detail"),
    path("teacher/courses/<int:course_id>/enrollments/<int:enrollment_id>/update-level/", views.update_student_level, name="update_student_level"),

    path("teacher/calendar/", views.teacher_calendar, name="teacher_calendar"),
    path("teacher/calendar/events/", views.teacher_calendar_events, name="teacher_calendar_events"),

    
    path("teacher/teacher_profile_settings/", views.teacher_profile_settings, name="teacher_profile_settings"),    
]

