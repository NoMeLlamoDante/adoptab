from django.shortcuts import render, redirect
from .models import Pet
from .forms import PetForm


# Create your views here.
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = PetForm()

    context = {"title": "Mascotas", "form": form}
    return render(request, "pets/add_pet.html", context)
