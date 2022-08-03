from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser
from .token import token_generator


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
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'position')


class CustomLoginCreateForm(AuthenticationForm):
    username = forms.EmailField(label="Електрона пошта",
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': "Email не зареєстровано або не підтверджений.Перевірте пошту."
    }

    class Meta:
        model = User
        fields = ('username', 'password')
