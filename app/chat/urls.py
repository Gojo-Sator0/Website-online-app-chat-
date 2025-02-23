
from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.chats_view, name='chats'),  # Список чатов
    path('chat/room/<str:chatroom_name>/', views.chats_view, name='chatroom'),  # Конкретный чат
    path('chat/edit/<str:chatroom_name>/', views.chatroom_edit_view, name='edit-group'),  # Редактирование группы
    path('search-users/', views.search_users, name='search-users'),
    path('chat/chatroom-leave/<str:chatroom_name>/', views.chatroom_leave_view, name='chatroom-leave'),  # Выход из чата
    path('chat/new-groupchat/', views.create_groupchat, name='new-groupchat'),  # Создание группы
    path('chat/user/<str:username>/', views.get_or_create_chatroom, name='start-chat'),  # Приватный чат с пользователем
    path('chat/fileupload/<str:chatroom_name>', views.chat_file_upload, name='chat-file-upload'),  
]
