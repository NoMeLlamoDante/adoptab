from datetime import date
from typing import Optional
from pets.utils.errors import PetError

from pets.models import Pet, Ownership, PetLogs, OwnerLogs
from django.contrib.auth.models import User


class PetService:
    def __init__(self) -> None:
        pass

    def createPet(
        self,
        *,
        user: User,
        name: str,
        birth_date: date,
        species: str,
        breed: str,
        sex: str,
        color: str,
        hair: str,
        size: str,
        bio: str,
    ) -> Optional[Pet | None]:
        # Verificar variables
        if not name or len(name) > 100:
            raise PetError('El nombre debe estar entre 1 y 100 caracteres')
        if not birth_date:
            raise PetError('Fecha de nacimiento inválida')
        if species not in Pet.SPECIES_CHOICES:
            raise PetError('Valor de especie inválido')
        if not breed or len(breed) > 50:
            raise PetError(
                'La raza de la mascota debe estar entre 1 y 50 caracteres')
        if not color or len(color) > 50:
            raise PetError(
                'La color de pelo de la mascota debe estar entre 1 y 50 caracteres')
        if not bio or len(bio) > 250:
            raise PetError('el texto debe estar entre 1 y 250 caracteres')

        if sex not in Pet.SEX_CHOICES:
            raise PetError('Valor de sexo inválido')
        if size not in Pet.SIZE_CHOICES:
            raise PetError('Valor de tamaño inválido')
        if hair not in Pet.HAIR_CHOICES:
            raise PetError('Valor de sexo inválido')

        pet = None
        try:
            pet = Pet.objects.create(
                name=name,
                birth_date=birth_date,
                species=species,
                breed=breed,
                sex=sex,
                color=color,
                hair=hair,
                size=size,
                bio=bio,
                in_adopt=True,
                status='OK'
            )

            PetLogs.objects.create(
                pet=pet,
                action="create",
                user=user
            )

            ownership = Ownership.objects.create(
                pet=pet,
                owner=user
            )

            OwnerLogs.objects.create(
                ownership=ownership,
                action="create",
                user=user
            )

        except Exception as e:
            raise PetError('No fue posible completar la operación') from e

        return pet


class OwnerService:
    def __init__(self) -> None:
        pass
