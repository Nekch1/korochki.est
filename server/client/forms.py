from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'full_name', 'phone', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]{6,}$', username):
            raise forms.ValidationError(
                'Логин должен содержать минимум 6 символов (латиница и цифры)'
            )
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError(
                'Пароль должен содержать минимум 8 символов'
            )
        return password

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[А-Яа-яЁё\s]+$', full_name):
            raise forms.ValidationError(
                'ФИО должно содержать только кириллицу и пробелы'
            )
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError(
                'Телефон должен быть в формате 8(XXX)XXX-XX-XX'
            )
        return phone


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={})
    )