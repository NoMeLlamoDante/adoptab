from django.contrib import admin
from django.urls import path
from .views import add_pet, index, update_pet
from django.views.generic import TemplateView


urlpatterns = [
    path('', index, name="index"),
    path('add', add_pet, name="add_pet"),
    path('update/<int:id>', update_pet, name="update_pet"),

]
