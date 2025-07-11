from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.core.mail import send_mail
from django.template.loader import render_to_string
from adoptab import settings

from .tokens import user_activation_token
from .models import User


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
