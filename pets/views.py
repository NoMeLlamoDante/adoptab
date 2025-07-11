from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet
from .forms import PetForm
from django.contrib.auth.decorators import login_required

# Create your views here


def index(request):
    """Lista de mascotas """
    pets = Pet.objects.all()
    context = {"title": "Lista Mascotas", "pets": pets}
    return render(request, "pets/index.html", context)


@login_required
def add_pet(request):
    """ Vista para añadir nuevas mascotas"""
    form = PetForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            pet = form.save(commit=False)
            pet.status = 'OK'
            pet.size = 'M'
            pet.owner = request.user
            pet.save()
            return redirect('pets:index')

    context = {"title": "Nueva mascota", "form": form}
    return render(request, "pets/add_pet.html", context)


def detail_pet(request, id):
    """Vista de datos de mascota"""
    pet = get_object_or_404(Pet, pk=id)
    context = {
        "title": pet.name,
        "pet": pet
    }
    return render(request, "pets/detail_pet.html", context)


@login_required
def update_pet(request, id):
    """Actualizar datos de mascota """
    pet = get_object_or_404(Pet, pk=id)
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)

    if request.method == 'POST':
        if form.is_valid():
            if "file-clear" in request.POST:
                pet.file.delete(save=True)
            form.save()
            return redirect('pets:index')
        else:
            print(form.errors)
    context = {
        "title": "Actualizar Datos",
        "form": form,
        "pet": pet
    }
    return render(request, "pets/update_pet.html", context)


@login_required
def delete_pet(request, id):
    """Eliminar Mascota"""
    pet = get_object_or_404(Pet, id=id)
    pet.file.delete(save=False)
    pet.delete()
    return redirect('pets:index')
