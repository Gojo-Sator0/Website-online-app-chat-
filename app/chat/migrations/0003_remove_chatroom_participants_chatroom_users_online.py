# Generated by Django 5.1.5 on 2025-02-15 14:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_options_alter_message_context'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='participants',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='users_online',
            field=models.ManyToManyField(blank=True, related_name='online_in_group', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
    ]
