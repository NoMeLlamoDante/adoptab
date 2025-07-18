from django.urls import path
from .views import register_view, profile_view, profile_update, delete_view
from .views import login_view, logout_view, password_change_view
from .views import activate_view, password_reset_view, new_password_view


app_name = "users"

urlpatterns = [
    # Crud
    path('register/', register_view, name="register"),
    path('profile/', profile_view, name="profile"),
    path('update/', profile_update, name="profile_update"),
    path('delete/', delete_view, name="profile_delete"),

    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    path('password_change', password_change_view, name="password_change"),
    path('activate/<uidb64>/<token>/', activate_view, name="activate"),
    path('password_reset/', password_reset_view, name="password_reset"),
    path('password_reset/<uidb64>/<token>/',
         new_password_view, name="new_password"),
]
