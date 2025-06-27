from django.forms import ModelForm, Textarea
from .models import Pet


class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "birth_date", "species",
                  "breed", "sex", "color", "hair", "size", "bio"]
        widgets = {
            "bio": Textarea(attrs={
                "cols": 80,
                "rows": 10,
            }),
        }
