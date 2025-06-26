from django.db import models


SPECIES_CHOICES = {
    "cat": "Gato",
    "dog": "Perro"}
SEX_CHOICES = {
    "M": "Macho",
    "F": "Hembra"}
SIZE_CHOICES = {
    'S': 'Chico',
    'M': 'Mediano',
    'L': 'Grande'}
HAIR_CHOICES = {
    'S': 'Corto',
    'M': 'Mediano',
    'L': 'Largo'}
STATUS_CHOICES = {
    'OK': 'Normal',
    'SK': 'Enfermo',
    'DF': 'Fallecido'}


# Create your models here.
class Pet(models.Model):
    name = models.CharField(
        "Nombre", max_length=100)
    birth_date = models.DateField(
        "Fecha nacimiento", help_text="DD/MM/AAAA",
        blank=True, null=True)
    species = models.CharField(
        "Especie", max_length=3,
        choices=SPECIES_CHOICES, default="Gato")
    breed = models.CharField(
        "Raza", max_length=50,
        blank=True)
    sex = models.CharField(
        "Sexo", max_length=1,
        choices=SEX_CHOICES, default="Macho")
    color = models.CharField(
        max_length=50)
    hair = models.CharField(
        "Pelaje", max_length=50,
        choices=HAIR_CHOICES, default="M",
        blank=True)
    size = models.CharField(
        "Tamaño", max_length=1,
        choices=SIZE_CHOICES, default="M")
    in_adopt = models.BooleanField(
        "En Adopción",
        default=False,)
    bio = models.TextField(
        max_length=250,
        help_text="Datos de la mascota")
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES, default="Normal")
    owner = models.CharField(
        "Dueño", max_length=50,
        blank=True)

    def __str__(self):
        return f"{self.species} - {self.name} {"- en adopcion" if self.in_adopt else ""}"
