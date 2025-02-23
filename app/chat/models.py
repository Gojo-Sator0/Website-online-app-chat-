import os
from django.db import models
from django.conf import settings
import shortuuid
# Create your models here.

class ChatRoom(models.Model):
    
    name = models.CharField(max_length=255, verbose_name='Название', blank=True, null=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=255, verbose_name='Название', blank=True, null=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='group_chat', blank=True, null=True, on_delete=models.SET_NULL)
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
    context = models.CharField(verbose_name='Сообщение', max_length=300, blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', verbose_name='Файл', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        db_table = 'message'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-timestamp']

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None

    def __str__(self):
        if self.context:
            return f"{self.sender.username}: {self.context[:20]}"
        elif self.file:
            return f"{self.sender.username}: {self.filename}"
        
    @property
    def is_image(self):
        if self.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
            return True
        else:
            return False
            