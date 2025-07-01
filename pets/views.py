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

    context = {"title": "Nueva mascota", "form": form}
    return render(request, "pets/add_pet.html", context)


def index(request):

    pets = Pet.objects.all()
    context = {"title": "Lista Mascotas", "pets": pets}
    return render(request, "pets/index.html", context)
