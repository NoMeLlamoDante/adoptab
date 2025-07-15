from django.contrib import admin
from django.urls import path
from .views import index, add_pet, detail_pet, update_pet, delete_pet
from .views import photo_add_view, list_photo_view, photo_delete_view, photo_update_view
from django.views.generic import TemplateView

app_name = "pets"

urlpatterns = [
    path('', index, name="index"),

    path('add', add_pet, name="add_pet"),
    path('detail/<int:id>', detail_pet, name="detail_pet"),
    path('update/<int:id>', update_pet, name="update_pet"),
    path('delete/<int:id>', delete_pet, name="delete_pet"),

    path('photo/add/<int:id>', photo_add_view, name="add_photo"),
    path('photo/<int:id>', list_photo_view, name="list_photo"),
    path('photo/update/<int:id>', photo_update_view, name="update_photo"),
    path('photo/delete/<int:id>', photo_delete_view, name="delete_photo"),
]
