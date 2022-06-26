from django.db import models

from account.models import Account

# Create your models here.
class ChatRoom(models.Model):
    # Each chat chat has it's name.
    name = models.CharField(max_length=30)


class ChatRoomUsers(models.Model):
    # Group of users is assigned to singel chat.
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    # There can be many users in a single chatgroup.
    user = models.ForeignKey(Account, on_delete=models.PROTECT)


class Message(models.Model):
    # Each message has maximal length.
    text = models.CharField(max_length=1000)
    # Each message was sent at some time.
    pub_date = models.DateTimeField(auto_now_add=True)
    # Each message was sent by a user.
    user = models.ForeignKey(Account, on_delete=models.PROTECT)
    # Each message is assigned to some chatroom.
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)


class FriendshipRelation(models.Model):
    # Every user has his own FriendshipRelation.
    user = models.ForeignKey(
        Account,
        related_name="senders",
        on_delete=models.PROTECT,
    )
    # User can have many friends.
    friend = models.ForeignKey(
        Account, 
        related_name="receivers",
        on_delete=models.PROTECT
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'friend'], 
                name="unique_friendrelation"
            )
        ]
