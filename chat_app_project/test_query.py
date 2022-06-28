from chat_app.models import ChatRoom, ChatRoomUsers
from account.models import Account


user = Account.objects.get(id=1)
friend = Account.objects.get(id=2)

chatroom_friend = ChatRoomUsers.objects.filter(
    user_id=friend.id,
    chatroom__is_private=True
).values("chatroom__id")

chatroom_users = ChatRoomUsers.objects.filter(
    user_id=user.id,
    chatroom__is_private=True,
    chatroom__id__in=chatroom_friend
)

print(chatroom_users.count())

# print(chatroom_users.chatroomusers_set.all().values("user"))