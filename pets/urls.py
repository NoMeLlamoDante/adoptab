from django.contrib import admin
from django.urls import path
from .views import add_pet
from django.views.generic import TemplateView


urlpatterns = [
    path('add', add_pet, name="add_pet")
]
