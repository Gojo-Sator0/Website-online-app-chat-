from django import forms
from django.forms import ModelForm
from .models import * 

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = ['context']
        
        context = forms.CharField()

class NewGroupForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['groupchat_name']
        
        groupchat_name = forms.CharField()
        