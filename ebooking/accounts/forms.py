from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.forms import ModelChoiceField, Select

INVALID_CREDS_MSG = "Credențialele introduse sunt greșite."

User = get_user_model()

class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': _('Introduceti parola')}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_(INVALID_CREDS_MSG))

        return password



class SignInViaEmailForm(SignIn):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type': 'email', 'placeholder': _('Adresa de email')}))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(SignInViaEmailForm, self).__init__(*args, **kwargs)
        print("init sign in via form")
        # self.fields['email'].widget.attrs['placeholder'] = "Introduceti emailul..."

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).first()
       
        if not user:
            raise ValidationError(_(INVALID_CREDS_MSG))

        self.user_cache = user

        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('phone',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs['placeholder'] = "Introduceți numarul de telefon"


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=_('Email'),
                             error_messages={'required': 'Introduceți o adresă de mail validă!'},
                             required=True)

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()

        if user:
            raise ValidationError(_('Nu puteți folosi această adresă de email!'))

        return email

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.error_messages['password_mismatch'] = "Parolele din cele două câmpuri trebuie să fie identice!"

        self.fields['first_name'].label = ""
        self.fields['first_name'].required = True
        self.fields['last_name'].label = ""
        self.fields['last_name'].required = True
        self.fields['email'].label = ""
        self.fields['email'].required = True
        self.fields['password1'].label = ""
        # self.fields['password1'].help_text = ""
        self.fields['password1'].required = True
        self.fields['password2'].label = ""
        self.fields['password2'].help_text = ""
        self.fields['password2'].required = True

        self.fields['first_name'].widget.attrs['placeholder'] = "Introduceți prenumele"
        self.fields['last_name'].widget.attrs['placeholder'] = "Introduceți numele"
        self.fields['email'].widget.attrs['placeholder'] = "Introduceți adresa de email"
        self.fields['password1'].widget.attrs['placeholder'] = "Introduceți parola"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirmați parola"




class RestorePasswordForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_("Adresă de e-mail invalidă!"))

        self.user_cache = user

        return email


class RestorePasswordViaEmailOrUsernameForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_('Email or Username'))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_("Adresă de e-mail invalidă!"))

        self.user_cache = user

        return email_or_username

 
class ChangeProfileForm(forms.Form):
    phone = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].label = "Phone Number"

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == self.user.email:
            raise ValidationError(_('Please enter another email.'))

        user = User.objects.filter(Q(email__iexact=email) & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('You can not use this mail.'))

        return email
