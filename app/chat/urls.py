
from django.urls import path

from chat import views

urlpatterns = [
    path('chats/', views.chats_view, name='chats'),
]