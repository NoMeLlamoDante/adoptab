from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
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
            user = form.get_user()
            login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect('pets:index')

    context = {
        "title": "iniciar sesion",
        "form": form,
        "next": request.GET.get('next'),
    }
    return render(request, "users/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')
