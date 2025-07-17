from django.shortcuts import render, redirect, get_object_or_404

from .models import Pet, Photo, User, Ownership
from .forms import OwnerForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django.contrib import messages


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
    user = get_object_or_404(User, id=request.user.id)

    messages.add_message(request, messages.SUCCESS,
                         "Usuario eliminado correctamente")
    return redirect('users:login')
