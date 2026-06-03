from django.urls import path

from . import views

urlpatterns = [
    path("welcome/", views.welcome, name="welcome"),
    path("cakes/", views.cake_list, name="cake_list"),
    path("cakes/<slug:slug>/", views.cake_detail, name="cake_detail"),
    path("cart/", views.cart, name="cart"),
    path("plan-order/", views.plan_order, name="plan_order"),
    path("demo-checkout/", views.demo_checkout, name="demo_checkout"),
    path("offers/", views.offers, name="offers"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
