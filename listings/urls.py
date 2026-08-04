from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("edit/<str:property_id>/", views.edit_property, name="edit_property"),
    path("delete/<str:property_id>/", views.delete_property, name="delete_property"),
    path("average-report/", views.average_rent_report, name="reports"),
    path("api/properties/", views.property_api, name="property_api"),
]