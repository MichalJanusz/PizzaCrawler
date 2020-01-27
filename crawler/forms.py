from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    login = forms.CharField(max_length=128, label='Login')
    password = forms.CharField(max_length=128, label='Hasło', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Login', max_length=64)
    password = forms.CharField(label='Hasło', max_length=64, widget=forms.PasswordInput)
    re_password = forms.CharField(label='Powtórz Hasło', max_length=64, widget=forms.PasswordInput)
    first_name = forms.CharField(label='Imię', max_length=128)
    last_name = forms.CharField(label='Nazwisko', max_length=128)
    email = forms.EmailField(label='e-mail')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        username = cleaned_data.get('username')
        db_username = User.objects.filter(username=username)

        if len(db_username) > 0:
            raise ValidationError('login juz istnieje')

        if password != re_password:
            raise ValidationError('hasła niezgodne')