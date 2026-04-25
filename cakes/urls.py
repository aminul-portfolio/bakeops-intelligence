from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("welcome/", views.welcome, name="welcome"),
    path("cakes/", views.cake_list, name="cake_list"),
    path("cakes/<slug:slug>/", views.cake_detail, name="cake_detail"),
    path("offers/", views.offers, name="offers"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
