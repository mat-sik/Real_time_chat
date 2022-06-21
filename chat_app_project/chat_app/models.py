from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    # Each message has maximal length.
    text = models.CharField(max_length=1000)
    # Each message was sent at some time.
    pub_date = models.DateTimeField(auto_now_add=True)
    # Each message was sent by a user
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class ChatRoom(models.Model):
    # There can be many users in a single chatroom.
    users = models.ForeignKey(User, on_delete=models.PROTECT)
    # Each chat room will have its own corresponding messages,
    # that will be displayed by publication date order.
    messages = models.ForeignKey(Message, on_delete=models.CASCADE)


class FriendsList(models.Model):
    # Every user has his own friendslist.
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
    )
    # User can have many friends.
    friends = models.ForeignKey(User, on_delete=models.PROTECT)
