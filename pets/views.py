from django.shortcuts import render, redirect, get_object_or_404
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


def update_pet(request, id):
    pet = get_object_or_404(Pet, pk=id)
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    context = {
        "title": "Actualizar Datos",
        "form": form,
        "pet": pet
    }
    return render(request, "pets/update_pet.html", context)


def delete_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    pet.file.delete(save=False)
    pet.delete()
    return redirect('index')
