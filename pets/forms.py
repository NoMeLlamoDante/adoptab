from django import forms
from django.forms import ModelForm, Textarea

from .models import Pet
# choices
from .models import SPECIES_CHOICES, SEX_CHOICES
from .models import SIZE_CHOICES, HAIR_CHOICES, STATUS_CHOICES
from datetime import datetime


class PetForm(forms.ModelForm):
    year = datetime.now().year

    name = forms.CharField(
        label="Nombre",
        max_length=100)
    species = forms.ChoiceField(
        label="Especie",
        choices=SPECIES_CHOICES,
        widget=forms.RadioSelect, initial="cat")
    sex = forms.ChoiceField(
        label="Sexo",
        choices=SEX_CHOICES,
        widget=forms.RadioSelect,
        initial="M"
    )

    birth_date = forms.DateField(
        label="Fecha nacimiento",
        help_text="DD/MM/AAAA",
        widget=forms.SelectDateWidget(
            years=list(reversed(range(year-30, year+1)))),
        initial=datetime.now(),
    )
    bio = forms.CharField(
        help_text="Acerca de la mascota",
        max_length=250,
        required=False,
        widget=forms.Textarea(attrs={'rows': 5}),
    )

    breed = forms.CharField(
        label="Raza",
        max_length=50,
    )
    color = forms.CharField(
        max_length=50)
    hair = forms.ChoiceField(
        label="Pelaje",
        choices=HAIR_CHOICES,
        widget=forms.RadioSelect,
        initial="M",
    )

    class Meta:
        model = Pet
        fields = ["name", "species", "sex", "birth_date",
                  "bio", "breed", "color", "hair"]
