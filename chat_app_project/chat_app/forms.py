from django import forms
from django.db.utils import IntegrityError
from django.contrib import messages
from django.db import transaction

from account.models import Account
from chat_app.models import FriendshipRelation, ChatRoomUsers, ChatRoom


class AddFriendForm(forms.Form):
    friend_username = forms.CharField(max_length=30)

    def username_exists(self):
        friend_username = self.cleaned_data.get("friend_username")
        return Account.objects.filter(username=friend_username).count() > 0

    def is_initial_friend_request(self, user, friend):
        """If is inintial user wasn't sent friend request by some friend user."""
        return FriendshipRelation.objects.filter(user=friend, friend=user).count() == 0

    def private_chat_exists(self, user, friend):
        friends_cids = ChatRoomUsers.objects.filter(
            user_id=friend.id,
            chatroom__is_private=True
        ).values("chatroom__id")

        common_private_chat = ChatRoomUsers.objects.filter(
            user_id=user.id,
            chatroom__is_private=True,
            chatroom__id__in=friends_cids
        )
        return common_private_chat.count() == 1

    def save(self, request):
        user = request.user
        friend_username = self.cleaned_data.get("friend_username")
        friend = Account.objects.get(username=friend_username)

        if not user == friend:
            try:
                FriendshipRelation.objects.create(
                    user=user,
                    friend=friend
                )
                # creates private chat with user and friend if is initial
                # and private chat doesn't exist.
                if (self.is_initial_friend_request(user, friend) and
                        not self.private_chat_exists(user, friend)):

                    new_chatroom = ChatRoom.objects.create(
                        name = f"{user.username}-{friend.username}_chatroom"
                    )
                    ChatRoomUsers.objects.create(
                        chatroom = new_chatroom,
                        user = user
                    )
                    ChatRoomUsers.objects.create(
                        chatroom = new_chatroom,
                        user = friend
                    )
                messages.add_message(
                    request, 
                    messages.INFO, 
                    "Request sent."
                )
            except IntegrityError:
                messages.add_message(
                    request, 
                    messages.ERROR, 
                    "You are friends already."
                )
        else:
            messages.add_message(
                request, 
                messages.ERROR, 
                "You can not add yourself as friend."
            )    


class AddChatRoomForm(forms.Form):
    chat_name = forms.CharField(max_length=30)
    def __init__(self, request, friends=None, *args, **kwargs):
        super(AddChatRoomForm, self).__init__(*args, **kwargs)
        if friends is None:
            # Ids of users who were sent friend request by current user.
            sent_requests_uid = FriendshipRelation.objects.filter(
                user=request.user
            ).values("friend_id")

            # Ids of users who are friends with current user.
            friends_uid = FriendshipRelation.objects.filter(
                friend=request.user # aquired friend request of current user.
            ).filter(user_id__in=sent_requests_uid).values("user_id")

            # Users who are friends with current user.
            friends = Account.objects.filter(
                id__in=friends_uid
            )

        self.fields['users'] = forms.ModelMultipleChoiceField(
            queryset=friends,
            required=True
        )

    @transaction.atomic
    def save(self, request):
        new_chatroom = ChatRoom.objects.create(
            name = self.cleaned_data.get("chat_name"),
            is_private = False
        )
        ChatRoomUsers.objects.create(
            chatroom = new_chatroom,
            user = request.user
        )
        for user in self.cleaned_data.get("users"): # type: ignore
                ChatRoomUsers.objects.create(
                    chatroom = new_chatroom,
                    user = user
                )
