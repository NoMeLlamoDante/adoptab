from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout


# Create your views here.
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pets:index')
    context = {
        "title": "nuevo usuario",
        "form": form,
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("valid")
            user = form.get_user()
            login(request, user)
            return redirect('pets:index')
    return render(
        request, "users/login.html", {"title": "iniciar sesion", "form": form})


def logout_view(request):
    logout(request)
    return redirect('users:login')
