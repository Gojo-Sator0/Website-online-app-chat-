# Generated by Django 5.1.5 on 2025-02-07 15:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('chat_type', models.CharField(choices=[('private', 'Private'), ('group', 'Group')], default='private', max_length=10, verbose_name='Тип чата')),
                ('participants', models.ManyToManyField(related_name='chat_rooms', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'db_table': 'chat_room',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField(verbose_name='Сообщение')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatroom', verbose_name='Чат')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'db_table': 'message',
            },
        ),
    ]
