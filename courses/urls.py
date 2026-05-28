from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("my-calendar/", views.my_calendar, name="my_calendar"),
    path("my-calendar/events/", views.my_calendar_events, name="my_calendar_events"),
]