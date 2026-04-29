from django.urls import path

from . import views

app_name = "bakeops"


urlpatterns = [
    path("", views.analytics_dashboard, name="analytics-dashboard"),
    path("products/", views.product_profitability, name="product-profitability"),
    path("ingredients/", views.ingredient_risk, name="ingredient-risk"),
    path("waste/", views.waste_analysis, name="waste-analysis"),
    path("occasions/", views.occasion_analytics, name="occasion-analytics"),
    path("customers/", views.customer_analytics, name="customer-analytics"),
    path("data-quality/", views.data_quality_review, name="data-quality-review"),
    path("exports/", views.export_centre, name="export-centre"),
]