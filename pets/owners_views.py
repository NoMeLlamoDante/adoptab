from datetime import date
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.contrib import messages

from .models import Pet, User, Ownership
from .forms import OwnerForm


@login_required
@require_http_methods(["GET", "POST"])
def owner_list_view(request, id):
    """Vista de dueños de mascota"""
    pet = get_object_or_404(Pet, pk=id)

    owners = Ownership.objects.all().filter(
        pet=pet, validated=True).order_by("start_date")

    form = OwnerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            user = get_object_or_404(User, email=form.cleaned_data["owner"])
            Ownership.objects.create(pet=pet, owner=user)
            messages.add_message(
                request, messages.SUCCESS,
                "Solicitud enviada, espere a que el usuario acepte")
            return redirect("pets:owner_list", id=pet.id)
        except Exception as e:
            messages.add_message(request, messages.WARNING,
                                 "Usuario no encontrado")
    context = {
        "title": f"dueños de {{pet.name}}",
        "pet": pet,
        "owners": owners,
        "form": form,
    }
    return render(request, "pets/pet_owners.html", context)


@login_required
@require_http_methods(["GET"])
def end_ownership(request, id):
    """Dejar de ser dueño de una mascota"""
    try:
        ownership = get_object_or_404(Ownership, id=id)
        ownership.end_date = date.today()
        ownership.save()
        messages.add_message(request, messages.SUCCESS,
                             "datos actualizados")
    except Exception:
        messages.add_message(request, messages.ERROR,
                             "error en la transacción")
    return redirect('pets:owner_list', id=ownership.pet.id)


@login_required
@require_http_methods(["GET"])
def my_pets_view(request):
    """Lista de mascotas asociadas a mi"""
    pets = Pet.objects.filter(
        ownership__owner=request.user,
        ownership__validated=True,
        ownership__end_date=None,
    )
    pet_requests = Pet.objects.filter(
        ownership__owner=request.user,
        ownership__validated=False,
        ownership__end_date=None,
    )
    context = {
        "title": "Mis Mascotas",
        "pets": pets,
        "request": pet_requests,
        "url_prev": request.META.get('HTTP_REFERER'),
    }
    return render(request, "pets/my_pets.html", context)


@login_required
@require_http_methods(["GET"])
def adoption(request, id):
    """Poner mascota en adopción"""
    pet = get_object_or_404(Pet, id=id)
    pet.in_adopt = True
    pet.save()
    return redirect('pets:index')


@login_required
@require_http_methods(["GET"])
def adopted(request, id):
    """Completar adopción de mascota"""
    pet = get_object_or_404(Pet, id=id)
    pet.in_adopt = False
    pet.save()
    return redirect('pets:owner_list', id=pet.id)
