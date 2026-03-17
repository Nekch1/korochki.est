from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    full_name = forms.CharField(label='ФИО')
    phone = forms.CharField(label='Телефон')
    email = forms.EmailField(label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'full_name', 'phone', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]{6,}$', username):
            raise forms.ValidationError(
                'Логин должен содержать минимум 6 символов (латиница и цифры)'
            )
        return username

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