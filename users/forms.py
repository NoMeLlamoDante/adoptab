from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """Formulario para captura de usuario nuevo"""
    first_name = forms.CharField(label="Nombre", max_length=50, required=False)
    last_name = forms.CharField(
        label="Apellido", max_length=50, required=False)
    email = forms.EmailField(label="Correo electrónico", required=True)
    phone = forms.CharField(label="Telefono", max_length=15, required=True)
    bio = forms.CharField(
        label="Acerca de", max_length=250, required=False,
        widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "email", "phone", "bio"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data['phone'],
                    'bio':  self.cleaned_data['bio']
                }
            )
        return user


class UpdateUserForm(forms.ModelForm):
    """Formulario para actualizar datos de usuario"""
    first_name = forms.CharField(label="Nombre", max_length=50, required=False)
    last_name = forms.CharField(
        label="Apellido", max_length=50, required=False)
    email = forms.EmailField(label="Correo Electrónico", required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name",
                  "email"]


class UpdateProfileForm(forms.ModelForm):
    """Actualización de datos de perfíl"""
    phone = forms.CharField(
        label="Telefono", max_length=15, required=True)
    bio = forms.CharField(
        label="Acerca de", max_length=250, required=False,
        widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Profile
        fields = ["phone", "bio"]
