from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User


SPECIES_CHOICES = [
    ("cat", "Gato"),
    ("dog", "Perro"),
]
SEX_CHOICES = [
    ("M", "Macho"),
    ("F", "Hembra"),
]
SIZE_CHOICES = [
    ('S', 'Chico'),
    ('M', 'Mediano'),
    ('L', 'Grande'),
]
HAIR_CHOICES = [
    ('S', 'Corto'),
    ('M', 'Mediano'),
    ('L', 'Largo'),
]
STATUS_CHOICES = [
    ('OK', 'Normal'),
    ('SK', 'Enfermo'),
    ('DF', 'Fallecido'),
]


# Create your models here.
class Pet(models.Model):
    """Pet Basic info"""
    name = models.CharField(max_length=100)
    birth_date = models.DateField(
        help_text="DD/MM/AAAA", blank=True, null=True)
    species = models.CharField(
        max_length=3, choices=SPECIES_CHOICES,
        default=SPECIES_CHOICES[0])
    breed = models.CharField(max_length=50, blank=True)
    sex = models.CharField(
        max_length=5, choices=SEX_CHOICES, default=SEX_CHOICES[0])
    color = models.CharField(max_length=50)
    hair = models.CharField(
        max_length=1, choices=HAIR_CHOICES,
        default=HAIR_CHOICES[1], blank=True)
    size = models.CharField(
        max_length=1, choices=SIZE_CHOICES,
        default=SIZE_CHOICES[1], blank=True, null=True)
    in_adopt = models.BooleanField(default=True)
    bio = models.TextField(max_length=250, help_text="Datos de la mascota")
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=STATUS_CHOICES[1],
        blank=False, null=True)
    owners = models.ManyToManyField(
        User, through='Ownership', related_name='owned_pets')

    def __str__(self):
        return f"{self.species} - {self.name}"

    @property
    def pet_age(self):
        """Human pet age in text, in months, years and months or months only"""
        today = date.today()
        delta = relativedelta(today, self.birth_date)
        if delta.years >= 2:
            return f"{delta.years} años"
        elif delta.years >= 1:
            return f"{delta.years} años {delta.months} meses"
        else:
            age_in_months = delta.years * 12 + delta.months
            return f"{age_in_months} meses"


class Photo(models.Model):
    """Different photo for a pet"""
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="photos")
    file = models.ImageField(upload_to="pets/photo")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.pet.name}"


# class Service(models.Model):
#     """An agend to save pets info"""
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     role = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.name} - {self.role}"


class Ownership(models.Model):
    """A model saving ownership info"""
    pet = models.ForeignKey(Pet, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    validated = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('pet', 'owner', 'start_date')

    def __str__(self):
        return f"{self.pet.name} - {self.owner} ({self.start_date} - {self.end_date or ""})"
