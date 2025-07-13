from django.urls import path
from .views import register_view, profile_view
from .views import login_view, logout_view
from .views import activate_view, password_reset_view, new_password_view


app_name = "users"

urlpatterns = [
    # Crud
    path('register/', register_view, name="register"),
    path('profile/', profile_view, name="profile"),

    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    path('activate/<uidb64>/<token>/', activate_view, name="activate"),
    path('password_reset/', password_reset_view, name="password_reset"),
    path('password_reset/<uidb64>/<token>/',
         new_password_view, name="new_password"),
]
