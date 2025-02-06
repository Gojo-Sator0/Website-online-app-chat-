from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import User

class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()

    # Первый вариант ПРИМЕР
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={'autofocus': True,
    #                                   'class': 'form-control',}))
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
    #                                       'class': 'form-control',}),)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'phone_number', 
            'password1', 
            'password2'
            ]
        
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    phone_number = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    