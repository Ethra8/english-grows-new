from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),

    path("profile_settings/", views.profile_settings, name="profile_settings"),    
    path("student/my_course/", views.my_course, name="my_course"),
    path("student/my_attendance/", views.my_attendance, name="my_attendance"),
    path("student/my_calendar/", views.my_calendar, name="my_calendar"),
    path("student/my_calendar/events/", views.my_calendar_events, name="my_calendar_events"),

    path("teacher/teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/courses/", views.teacher_courses, name="teacher_courses"),
    path("teacher/calendar/", views.teacher_calendar, name="teacher_calendar"),
    path("teacher/calendar/events/", views.teacher_calendar_events, name="teacher_calendar_events"),
    path("teacher/teacher_profile_settings/", views.teacher_profile_settings, name="teacher_profile_settings"),    
    path("teacher/teacher_attendance/", views.teacher_attendance, name="teacher_attendance"),
]

