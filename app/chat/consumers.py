import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from chat.models import ChatRoom, Message
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Получаем текущего пользователя из scope (области видимости)
        self.user = self.scope['user']
        # Извлекаем room_name из URL-маршрута
        self.chatroom_name = self.scope['url_route']['kwargs']['room_name']
        # Ищем комнату чата в базе данных по имени. Если комната не найдена, возвращаем 404.
        self.chatroom = get_object_or_404(ChatRoom, name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        # Принимаем WebSocket-соединение
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

    def receive(self, text_data):
        # Преобразуем полученные данные из JSON в словарь Python
        text_data_json = json.loads(text_data)
        # Извлекаем текст сообщения из данных
        context = text_data_json['context']
        # Создаем новое сообщение в базе данных
        message = Message.objects.create(
            context=context,  # Текст сообщения
            sender=self.user,  # Отправитель (текущий пользователь)
            chat=self.chatroom,  # Комната чата
        )

        event = {
            'type':'message_handler',
            'message_id':message.id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = Message.objects.get(id=message_id)
        context = {
            'message': message,  # Объект сообщения
            'user': self.user,  # Текущий пользователь
        }
        # Рендерим HTML-шаблон с использованием подготовленного контекста
        html = render_to_string("chat/includes/chat_message_p.html", context=context)
        # Отправляем отрендеренный HTML обратно клиенту через WebSocket
        self.send(text_data=html)