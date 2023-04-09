from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from random import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.shortcuts import render
from django.conf import settings

from .models import Profile
from .utils import send_reset_password_email         
from .forms import (
    SignInViaEmailForm, SignUpForm, RestorePasswordViaEmailOrUsernameForm, ChangeProfileForm, ProfileForm, 
    )


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'accounts/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        return SignInViaEmailForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)
        login(request, form.user_cache)
        if request.user.is_superuser:
             return redirect(reverse('admin:index'))
        else:
            return redirect("/home")

    def form_invalid(self, form):
        show_signup_errors(self.request, form)
        return redirect(settings.LOGIN_REDIRECT_URL)


def show_signup_errors(request, form):
    for error in form.errors.values():
        # Get error description
        error_msg = error.as_text().replace('*', ' ')
        # Show toast message
        messages.add_message(request, messages.ERROR, error_msg)


def get_rand():
    random_number = random.randint(0, 1000)
    return random_number

def signup_view(request):
    if request.user.is_authenticated:
        # Redirect authenticated user to home page
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid(): 
            user = user_form.save(commit=False)
            user.username = f'user_{user.last_name}_{user.first_name}_{get_rand()}'
            user.save()

            profile = Profile(user=user, phone=profile_form.cleaned_data["phone"])
         
            profile.save()
            user.save()

            messages.success(request,
                             _('Cont creat cu succes! Verificați inbox-ul pentru a vă confirma adresa de e-mail!'))

            return redirect('/')
        else:
            # Adaugare mesaje in functie de problemaFs
            if not user_form.is_valid():
                show_signup_errors(request, user_form)
            if not profile_form.is_valid():
                show_signup_errors(request, profile_form)
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, "accounts/sign_up.html", context={"user_form": user_form, "profile_form": profile_form})



class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'accounts/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        return RestorePasswordViaEmailOrUsernameForm

        # return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        messages.add_message(self.request, messages.SUCCESS,
                             'Veți primi un mesaj e-mail cu instrucțiunile necesare a vă reseta parola.')
        return redirect('accounts:restore_password_done')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['phone_number'] = user.profile.phone_number

        return initial

    def form_valid(self, form):
        user = self.request.user

        user.profile.phone_number = form.cleaned_data['phone_number']
        user.profile.save()

        messages.success(self.request, _('Preferințele dumneavoastră au fost actualizate.'))
        print(f"Form errors: {form.errors}")
        return redirect('accounts:change_profile')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'accounts/profile/change_password.html'

    def __init__(self, *args, **kwargs):
        super(ChangePasswordView, self).__init__()
        print("called")
        self.form_class.base_fields['old_password'].help_text = ''
        self.form_class.base_fields['old_password'].label = ''
        self.form_class.base_fields['old_password'].widget.attrs['placeholder'] = 'Parolă veche'

        self.form_class.base_fields['new_password1'].label = ''
        self.form_class.base_fields['new_password1'].widget.attrs['placeholder'] = 'Parolă nouă'

        self.form_class.base_fields['new_password2'].help_text = ''
        self.form_class.base_fields['new_password2'].label = ''
        self.form_class.base_fields['new_password2'].widget.attrs['placeholder'] = 'Confirmarea noii parole'

        for error in self.form_class.error_messages:
            print(error)

        self.form_class.error_messages['password_incorrect'] = "Parola veche nu este corectă!"
        self.form_class.error_messages['password_mismatch'] = "Parolele din cele două câmpuri trebuie să fie identice!"

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Parola dumneavoastră a fost schimbată.'))

        return redirect('accounts:change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'accounts/restore_password_confirm.html'

    def __init__(self, *args, **kwargs):
        super(RestorePasswordConfirmView, self).__init__(*args, **kwargs)

        self.form_class.error_messages['password_mismatch'] = "Parolele din cele două câmpuri trebuie să fie identice!"
        # self.form_class.error_messages['password_mismatch'].widget.attrs['class'] = 'dismissable fade show'

        self.form_class.base_fields['new_password1'].widget.attrs['placeholder'] = 'Noua parolă'
        self.form_class.base_fields['new_password2'].widget.attrs['placeholder'] = 'Confirmarea noii parole'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Parola dumneavoastră a fost actualizată, vă puteți autentifica.'))

        return redirect('accounts:log_in')


@method_decorator(login_required, name='dispatch')
class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'accounts/restore_password_done.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/log_out.html'