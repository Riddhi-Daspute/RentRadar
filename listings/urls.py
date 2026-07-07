from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("edit/<str:property_id>/", views.edit_property, name="edit_property"),
]