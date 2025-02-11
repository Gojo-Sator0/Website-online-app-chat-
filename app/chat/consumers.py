import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from chat.models import ChatRoom, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Получаем текущего пользователя из scope (области видимости)
        self.user = self.scope['user']
        # Извлекаем room_name из URL-маршрута
        self.chatroom_name = self.scope['url_route']['kwargs']['room_name']
        # Ищем комнату чата в базе данных по имени. Если комната не найдена, возвращаем 404.
        self.chatroom = get_object_or_404(ChatRoom, name=self.chatroom_name)
        # Принимаем WebSocket-соединение
        self.accept()

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
        # Подготавливаем контекст для рендеринга HTML-шаблона
        context = {
            'message': message,  # Объект сообщения
            'user': self.user,  # Текущий пользователь
        }
        # Рендерим HTML-шаблон с использованием подготовленного контекста
        html = render_to_string("chat/includes/chat_message_p.html", context=context)
        # Отправляем отрендеренный HTML обратно клиенту через WebSocket
        self.send(text_data=html)