from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, label='Login')
    password = forms.CharField(max_length=128, label='Hasło', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Zaloguj')
        )


class RegisterForm(forms.Form):
    username = forms.CharField(label='Login', max_length=64)
    password = forms.CharField(label='Hasło', max_length=64, widget=forms.PasswordInput)
    re_password = forms.CharField(label='Powtórz Hasło', max_length=64, widget=forms.PasswordInput)
    first_name = forms.CharField(label='Imię', max_length=128)
    last_name = forms.CharField(label='Nazwisko', max_length=128)
    email = forms.EmailField(
        label='e-mail',
        widget=forms.TextInput(attrs={'placeholder': 'przyklad@przyklad.com'})
    )
    city = forms.CharField(
        max_length=128,
        required=False,
        label='Miasto',
        widget=forms.TextInput(attrs={'placeholder': 'np. Warszawa'})
    )
    street = forms.CharField(
        max_length=256,
        required=False,
        label='Ulica', widget=forms.TextInput(attrs={'placeholder': 'np. Marszałkowska'})
    )
    house_nr = forms.IntegerField(
        required=False,
        label='nr. Domu',
        widget=forms.TextInput(attrs={'placeholder': '22'})
    )
    flat_nr = forms.IntegerField(
        required=False,
        label='nr. Mieszkania (opcjonalne)',
        widget=forms.TextInput(attrs={'placeholder': 'np. 137'})
    )
    phone_number = forms.IntegerField(
        required=False,
        label='nr. Telefonu',
        widget=forms.TextInput(attrs={'placeholder': '123456789'}),
        max_value=999999999
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username'),
                Column('email'),
                css_class='form-row'
            ),
            'password',
            're_password',
            Row(
                Column('first_name'),
                Column('last_name'),
                css_class='form-row'
            ),
            'phone_number',
            'city',
            Row(
                Column('street'),
                Column('house_nr'),
                Column('flat_nr'),
                css_class='form-row'
            ),
            Submit('submit', 'Zarejestruj')
        )
