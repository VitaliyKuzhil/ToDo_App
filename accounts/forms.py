from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError

from .models import CustomUser
from .tasks import send_email_celery


class CustomUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             max_length=50,
                             label="Електрона пошта",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 label="Ім'я",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                                max_length=50,
                                label="Фамілія",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.CharField(required=True,
                               max_length=100,
                               label="Позиція",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True,
                                label="Пароль",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True,
                                label="Повторіть пароль",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'position', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                                max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.CharField(required=True,
                               max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'position')


class CustomLoginCreateForm(AuthenticationForm):
    username = forms.EmailField(label="Електрона пошта",
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user = authenticate(
                self.request, username=username, password=password
            )
            if self.user is None:
                raise self.get_invalid_login_error()
            elif self.user.blocked:
                raise ValidationError(
                    'Ваш аккаунт заблоковано адміністратором',
                    code='blocked',
                )
            elif not self.user.is_active:
                send_email_celery.delay(
                    user_id=self.user.pk,
                    site_domain=get_current_site(self.request).domain
                )
                raise ValidationError(
                    'Перейдіть на електронну пошту та активуйте акаунт',
                    code='invalid',
                )

        return self.cleaned_data
