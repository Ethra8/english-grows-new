from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),
    path("profile_settings/", views.profile_settings, name="profile_settings"),
]