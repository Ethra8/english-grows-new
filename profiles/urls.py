from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),
    path("profile_settings/", views.profile_settings, name="profile_settings"),
    path("my_course/", views.my_course, name="my_course"),
    path("my_attendance/", views.my_attendance, name="my_attendance"),
    path("my-calendar/", views.my_calendar, name="my_calendar"),
    path("my-calendar/events/", views.my_calendar_events, name="my_calendar_events"),
]

