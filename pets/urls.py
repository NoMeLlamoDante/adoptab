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
from .owners_views import (owner_list_view,
                           end_ownership,
                           my_pets_view,
                           adoption,
                           adopted,
                           accept_request,
                           reject_request)

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

    path('owner/list/<int:id>', owner_list_view, name="owner_list"),
    path('owner/end/<int:id>', end_ownership, name="owner_end"),
    path('my_pets/', my_pets_view, name="my_pets"),

    path('in_adoption/<int:id>', adoption, name="pet_in_adoption"),
    path('adopted/<int:id>', adopted, name="pet_adopted"),

    path('owner/accept/<int:id>', accept_request, name="ownership_accept"),
    path('owner/reject/<int:id>', reject_request, name="ownership_reject"),
]
