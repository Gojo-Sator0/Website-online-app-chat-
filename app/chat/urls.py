
from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('chats/', views.chats_view, name='chats'),
]