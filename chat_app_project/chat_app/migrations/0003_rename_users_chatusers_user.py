# Generated by Django 4.0.5 on 2022-06-25 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0002_remove_chatroom_users_chatusers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatusers',
            old_name='users',
            new_name='user',
        ),
    ]