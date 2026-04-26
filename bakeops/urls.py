from django.urls import path

from . import views


app_name = "bakeops"


urlpatterns = [
    path("", views.analytics_dashboard, name="analytics-dashboard"),
]