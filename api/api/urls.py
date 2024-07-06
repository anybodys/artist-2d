from django.urls import path

from . import views

urlpatterns = [
    path("art", views.art, name="art"),
    path("health", views.health, name="health"),
]
