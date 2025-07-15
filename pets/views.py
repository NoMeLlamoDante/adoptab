from django.shortcuts import render, redirect, get_object_or_404

from .models import Pet, Photo
from .forms import PetForm, PhotoForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


# Create your views here
@require_http_methods(["GET"])
def index_view(request):
    """Lista de mascotas """
    pets = Pet.objects.all()
    context = {"title": "Lista Mascotas", "pets": pets}
    return render(request, "pets/index.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def pet_add_view(request):
    """ Vista para añadir nuevas mascotas"""
    form = PetForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        pet = form.save(commit=False)
        pet.status = 'OK'
        pet.owner = request.user
        pet.save()
        return redirect('pets:index')

    context = {"title": "Nueva mascota", "form": form}
    return render(request, "pets/pet_add.html", context)


@require_http_methods(["GET"])
def pet_detail_view(request, id):
    """Vista de datos de mascota"""
    pet = get_object_or_404(Pet, pk=id)
    photos = Photo.objects.filter(pet=pet) or None
    context = {
        "title": pet.name,
        "pet": pet,
        "photos": photos,
    }
    return render(request, "pets/pet_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def pet_update_view(request, id):
    """Actualizar datos de mascota """
    pet = get_object_or_404(Pet, pk=id)
    form = PetForm(request.POST or None instance=pet)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('pets:pet_detail', id=pet.id)
    context = {
        "title": "Actualizar Datos",
        "form": form,
        "pet": pet
    }
    return render(request, "pets/pet_update.html", context)


@login_required
@require_http_methods(["GET"])
def pet_delete(request, id):
    """Eliminar Mascota"""
    pet = get_object_or_404(Pet, id=id)
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
        return redirect('pets:photo_list', id=pet.id)

    context = {
        "title": f"Foto para {pet.name}",
        "pet": pet,
        "form": form,
    }
    return render(request, "pets/photo_add.html", context)


@login_required
@require_http_methods(["GET"])
def photo_list_view(request, id):
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
        return redirect('pets:photo_list', id=pet.id)

    context = {
        "title": f"Cambiar Foto de {pet.name}",
        "pet": pet,
        "photo": photo,
        "form": form,
    }
    return render(request, "pets/photo_update.html", context)


@login_required
@require_http_methods(["GET"])
def photo_delete(request, id):
    """Eliminar Mascota"""
    photo = get_object_or_404(Photo, id=id)
    id_pet = photo.pet.id
    photo.file.delete()
    photo.delete()
    return redirect('pets:photo_list', id=id_pet)
