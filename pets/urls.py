from django.contrib import admin
from django.urls import path
from .views import add_pet, index
from django.views.generic import TemplateView


urlpatterns = [
    path('', index, name="index"),
    path('add', add_pet, name="add_pet"),

]
