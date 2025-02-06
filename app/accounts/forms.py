from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={'autofocus': True,
    #                                   'class': 'form-control',}))
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
    #                                       'class': 'form-control',}),)

    class Meta:
        model = User
        fields = ['username', 'password']