from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.contrib import messages

from .models import Pet, Photo, Ownership
from .forms import PetForm, PhotoForm
from .services.service import PetService
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# Create your views here
@require_http_methods(["GET"])
def index_view(request):
    """Lista de mascotas """
    pets = Pet.objects.all().prefetch_related('photos').filter(in_adopt=True)
    context = {"title": "Lista Mascotas", "pets": pets}
    return render(request, "pets/index.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def pet_add_view(request):
    """ Vista para añadir nuevas mascotas"""
    form = PetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            service = PetService()
            pet = service.createPet(
                user=request.user,
                name=form.cleaned_data["name"],
                birth_date=form.cleaned_data["birth_date"],
                species=form.cleaned_data["species"],
                breed=form.cleaned_data["breed"],
                sex=form.cleaned_data["sex"],
                color=form.cleaned_data["color"],
                hair=form.cleaned_data["hair"],
                size=form.cleaned_data["size"],
                bio=form.cleaned_data["bio"],
            )
            messages.add_message(request, messages.SUCCESS,
                                 "Mascota creada")
        except Exception as e:
            print(e)
            messages.add_message(request, messages.error,
                                 "No es posible crear la mascota")
        return redirect('pets:index')

    context = {"title": "Nueva mascota", "form": form}
    return render(request, "pets/pet_add.html", context)


@require_http_methods(["GET"])
@cache_page(60*15)  # Seconds
def pet_detail_view(request, id):
    """Vista de datos de mascota"""
    pet = get_object_or_404(Pet.objects.prefetch_related('photos'), id=id)
    owners = Ownership.objects.filter(validated=True, pet=pet)
    context = {
        "title": pet.name,
        "pet": pet,
        "owners": owners,
    }
    return render(request, "pets/pet_detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def pet_update_view(request, id):
    """Actualizar datos de mascota """
    pet = get_object_or_404(Pet, pk=id)
    form = PetForm(request.POST or None, instance=pet)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             "Información actualizada")
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
@vary_on_cookie
@cache_page(60*15)  # Seconds
def photo_list_view(request, id):
    """Vista para agregar imágenes a las mascotas"""
    pet = get_object_or_404(Pet, pk=id)
    photos = Photo.objects.filter(pet=pet) or None
    context = {
        "title": f"Fotos de {pet.name}",
        "pet": pet,
        "photos": photos,
        "url_prev": request.META.get('HTTP_REFERER'),
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
