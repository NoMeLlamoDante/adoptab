from django.contrib import admin
from django.urls import path
from .views import index, add_pet, detail_pet, update_pet, delete_pet
from django.views.generic import TemplateView


urlpatterns = [
    path('', index, name="index"),
    path('add', add_pet, name="add_pet"),
    path('detail/<int:id>', detail_pet, name="detail_pet"),
    path('update/<int:id>', update_pet, name="update_pet"),
    path('delete/<int:id>', delete_pet, name="delete_pet"),
]
