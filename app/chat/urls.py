
from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.chats_view, name='chats'),
    path('chat/edit/<chatroom_name>', views.chatroom_edit_view, name='edit-group'),
    path('chat/chatroom-leave/<str:chatroom_name>/', views.chatroom_leave_view, name='chatroom-leave'),
    path('chat/room/<chatroom_name>', views.chats_view, name='chatroom'),
    path('chat/new-groupchat', views.create_groupchat, name='new-groupchat'),
    path('chat/<username>', views.get_or_create_chatroom, name='start-chat'),
]