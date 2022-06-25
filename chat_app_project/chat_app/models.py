from django.db import models

from account.models import Account

# Create your models here.
class Message(models.Model):
    # Each message has maximal length.
    text = models.CharField(max_length=1000)
    # Each message was sent at some time.
    pub_date = models.DateTimeField(auto_now_add=True)
    # Each message was sent by a user
    user = models.ForeignKey(Account, on_delete=models.PROTECT)


class ChatRoom(models.Model):
    # Each chat chat has it's name.
    chat_name = models.CharField(max_length=30)
    # There can be many users in a single chatroom.
    users = models.ForeignKey(Account, on_delete=models.PROTECT)
    # Each chat room will have its own corresponding messages,
    # that will be displayed by publication date order.
    messages = models.ForeignKey(Message, on_delete=models.CASCADE)


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
                name="unique_friendrelation")
        ]
