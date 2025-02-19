
from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.chats_view, name='chats'),
    path('chat/new-groupchat', views.create_groupchat, name='new-groupchat'),
    path('chat/<username>', views.get_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>', views.chats_view, name='chatroom'),
]