from django.urls import path
from . import views

app_name = "placement"

urlpatterns = [
    path("", views.placement_test, name="test"),
    path("result/", views.placement_result, name="result"),
]
