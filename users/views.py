from .models import User, Profile
from .tokens import user_activation_token, password_reset_token
from adoptab import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login, logout

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


# Create your views here.
@require_http_methods(["GET", "POST"])
def register_view(request):
    """Vista para registrar nuevos usaurios, incluye verificación via email"""
    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        # Email data
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = user_activation_token.make_token(user)
        activation_link = request.build_absolute_uri(
            reverse('users:activate', kwargs={
                    "uidb64": uidb64, "token": token})
        )
        text_message = render_to_string('users/email/activate_mail.html', {
            'user': user,
            'activation_url': activation_link
        })

        send_mail(
            subject="Activa tu cuenta",
            message=text_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        login(request, user)
        messages.add_message(request, messages.WARNING,
                             "Cuenta creada con éxito, Para activarla, revise el correo en su bandeja de SPAM")
        return redirect('pets:index')

    context = {
        "title": "nuevo usuario",
        "form": form,
    }

    return render(request, 'users/register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    form = AuthenticationForm(data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect('pets:index')

    context = {
        "title": "iniciar sesion",
        "form": form,
        "next": request.GET.get('next'),
    }
    return render(request, "users/login.html", context)


@login_required
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('users:login')


@require_http_methods(["GET"])
def activate_view(request, uidb64, token):
    """Activar el token enviado por correo"""

    try:
        uid = force_str(urlsafe_base64_decode(s=uidb64))
        user = get_object_or_404(User, pk=uid)

    except (TypeError, ValueError, OverflowError) as e:
        if not settings.DEBUG:
            messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user and user_activation_token.check_token(user, token):
        user.profile.email_confirmed = True
        user.save()
        messages.add_message(
            request, messages.SUCCESS,
            f'el usuario {request.user}, ha sido activado con éxito')
    else:
        messages.add_message(request, messages.WARNING,
                             "El link de activación es inválido.")
    return redirect('index')


@require_http_methods(["GET", "POST"])
def password_reset_view(request):
    """Vista para solicitar correo de recuperar contraseña"""
    form = PasswordResetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = request.POST.get("email")
        qs = User.objects.filter(email=email)

        if len(qs) > 0:
            # flags
            user = qs[0]
            user.profile.reset_password = True
            user.save()

            # Email data
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = password_reset_token.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('users:new_password', kwargs={
                        "uidb64": uidb64, "token": token})
            )
            text_message = render_to_string('users/email/reset_mail.html', {
                'user': user,
                'reset_url': reset_link
            })

            send_mail(
                subject="Recupera tu contraseña",
                message=text_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            messages.add_message(
                request, messages.WARNING,
                "El correo fue enviado con éxito, revise su carpeta de SPAM")
            return redirect("users:login")
        else:
            messages.add_message(
                request, messages.ERROR,
                "No se encuentra ninguna cuenta asociada a este correo")
    context = {
        "title": "Contraseña Olvidada",
        "form": form,
    }
    return render(request, "users/password_reset.html", context)


@require_http_methods(["GET", "POST"])
def new_password_view(request, uidb64, token):
    """Vista para establecer contraseña nueva"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

    except (TypeError, ValueError, OverflowError):
        messages.add_message(request, messages.WARNING, 'link inválido')
        user = None
        return redirect("users:login")

    finally:
        form = SetPasswordForm(user or None, request.POST or None)

    if user and request.method == "POST":
        if password_reset_token.check_token(user, token) and form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 "Contraseña cambiada con éxito")
            user.profile.reset_password = False
            user.save()
            return redirect("pets:index")
        else:
            messages.add_message(request, messages.WARNING, 'link inválido')
            return redirect("users:login")

    context = {
        'title': 'Nueva contraseña',
        'form': form,
        'uid': uidb64,
        'token': token
    }
    return render(request, "users/new_password.html", context)


@login_required
@require_http_methods(["GET"])
def profile_view(request):
    """Vista de detalles del usuario"""
    user = get_object_or_404(User, id=request.user.id)

    context = {
        "title": "iniciar sesion",
        "user_info": user,
    }
    return render(request, "users/profile_details.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def profile_update(request):
    """Editar datos del usuario"""
    user = get_object_or_404(User, id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=user)
    profile_form = UpdateProfileForm(
        request.POST or None, instance=user.profile)

    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.add_message(request, messages.SUCCESS,
                             "Se han guardado los cambios")
        return redirect('users:profile')

    context = {
        "title": "iniciar sesion",
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/profile_update.html", context)


@login_required
@require_http_methods(["GET"])
def delete_view(request):
    """Eliminar usuario"""
    user = get_object_or_404(User, id=request.user.id)
    print(user)
    user.delete()
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         "Usuario eliminado correctamente")
    return redirect('users:login')
