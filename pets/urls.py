from django.contrib import admin
from django.urls import path
from .views import index_view
from .views import (pet_add_view,
                    pet_detail_view,
                    pet_update_view,
                    pet_delete)
from .views import (photo_add_view,
                    photo_list_view,
                    photo_update_view,
                    photo_delete)

app_name = "pets"

urlpatterns = [
    path('', index_view, name="index"),

    path('add', pet_add_view, name="pet_add"),
    path('detail/<int:id>', pet_detail_view, name="pet_detail"),
    path('update/<int:id>', pet_update_view, name="pet_update"),
    path('delete/<int:id>', pet_delete, name="pet_delete"),

    path('photo/add/<int:id>', photo_add_view, name="photo_add"),
    path('photo/<int:id>', photo_list_view, name="photo_list"),
    path('photo/update/<int:id>', photo_update_view, name="photo_update"),
    path('photo/delete/<int:id>', photo_delete, name="photo_delete"),
]
