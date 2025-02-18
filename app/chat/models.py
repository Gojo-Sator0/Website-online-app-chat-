from django.db import models
from django.conf import settings
import shortuuid
# Create your models here.

class ChatRoom(models.Model):
    
    name = models.CharField(max_length=255, verbose_name='Название', blank=True, null=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Участники', related_name='online_in_group', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    class Meta: 
        db_table = 'chat_room'
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return self.name if self.name else f'Chat {self.id}'
    
class Message(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, verbose_name='Чат', related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Отправитель')
    context = models.CharField(verbose_name='Сообщение', max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        db_table = 'message'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.context[:20]}"