from django.shortcuts import render, redirect, get_object_or_404

from .models import Pet, Photo
from .forms import PetForm, PhotoForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


# Create your views here
@require_http_methods(["GET"])
def index(request):
    """Lista de mascotas """
    pets = Pet.objects.all()
    context = {"title": "Lista Mascotas", "pets": pets}
    return render(request, "pets/index.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def add_pet(request):
    """ Vista para añadir nuevas mascotas"""
    form = PetForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        pet = form.save(commit=False)
        pet.status = 'OK'
        pet.size = 'M'
        pet.owner = request.user
        pet.save()
        return redirect('pets:index')

    context = {"title": "Nueva mascota", "form": form}
    return render(request, "pets/add_pet.html", context)


@require_http_methods(["GET"])
def detail_pet(request, id):
    """Vista de datos de mascota"""
    pet = get_object_or_404(Pet, pk=id)
    photos = Photo.objects.filter(pet=pet) or None
    context = {
        "title": pet.name,
        "pet": pet,
        "photos": photos,
    }
    return render(request, "pets/detail_pet.html", context)


@login_required
@require_http_methods(["GET", "POST"])
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
    context = {
        "title": "Actualizar Datos",
        "form": form,
        "pet": pet
    }
    return render(request, "pets/update_pet.html", context)


@login_required
@require_http_methods(["GET"])
def delete_pet(request, id):
    """Eliminar Mascota"""
    pet = get_object_or_404(Pet, id=id)
    pet.file.delete(save=False)
    pet.delete()
    return redirect('pets:index')


@login_required
@require_http_methods(["GET", "POST"])
def photo_add_view(request, id):
    """Vista para agregar imágenes a las mascotas"""
    pet = get_object_or_404(Pet, pk=id)
    form = PhotoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        photo = form.save(commit=False)
        photo.pet = pet
        photo.save()
        return redirect('pets:list_photo', id=pet.id)

    context = {
        "title": f"Foto para {pet.name}",
        "pet": pet,
        "form": form,
    }
    return render(request, "pets/photo_form.html", context)


@login_required
@require_http_methods(["GET"])
def list_photo_view(request, id):
    """Vista para agregar imágenes a las mascotas"""
    pet = get_object_or_404(Pet, pk=id)
    photos = Photo.objects.filter(pet=pet) or None
    context = {
        "title": f"Fotos de {pet.name}",
        "pet": pet,
        "photos": photos,
    }
    return render(request, "pets/photo_list.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def photo_update_view(request, id):
    """Vista para agregar imágenes a las mascotas"""
    photo = get_object_or_404(Photo, pk=id)
    pet = photo.pet
    form = PhotoForm(
        request.POST or None, request.FILES or None, instance=photo)

    if request.method == 'POST' and form.is_valid():
        if "file-clear" in request.POST:
            photo.file.delete(save=True)
        form.save()
        return redirect('pets:list_photo', id=pet.id)

    context = {
        "title": f"Cambiar Foto de {pet.name}",
        "pet": pet,
        "photo": photo,
        "form": form,
    }
    return render(request, "pets/photo_update.html", context)


@login_required
@require_http_methods(["GET"])
def photo_delete_view(request, id):
    """Eliminar Mascota"""
    photo = get_object_or_404(Photo, id=id)
    id_pet = photo.pet.id
    photo.file.delete()
    photo.delete()
    return redirect('pets:list_photo', id=id_pet)
