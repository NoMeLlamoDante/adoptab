from django.urls import path
from .views import register_view, login_view, logout_view
from .views import activate_view

app_name = "users"

urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('activate/<uidb64>/<token>/', activate_view, name="activate"),
]
