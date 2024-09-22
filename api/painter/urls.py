from django.urls import path

from . import views

urlpatterns = [
    path("crontime", views.crontime, name="crontime"),
    path("health", views.health, name="health"),
]
