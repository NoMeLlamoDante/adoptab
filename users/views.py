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
            return redirect('index')
    context = {
        "title": "nuevo usuario",
        "form": form,
    }
    return render(request, 'users/register.html', context)
