from django import forms
from django.forms import ModelForm
from .models import * 

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = ['context']
        
        context = forms.CharField()