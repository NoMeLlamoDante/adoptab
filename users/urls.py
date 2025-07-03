from django.contrib import admin
from django.urls import path
from .views import register_view
from django.views.generic import TemplateView


urlpatterns = [
    path('register/', register_view, name="register"),
]
