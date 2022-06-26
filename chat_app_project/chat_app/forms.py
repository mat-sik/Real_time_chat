from django import forms
from django.db.utils import IntegrityError
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404

from account.models import Account
from chat_app.models import FriendshipRelation, ChatRoomUsers, ChatRoom


class AddFriendForm(forms.Form):
    friend_username = forms.CharField(max_length=30)

    def username_exists(self):
        friend_username = self.cleaned_data.get("friend_username")
        return Account.objects.filter(user_name=friend_username).count() > 0

    def save(self, request):
        user = request.user
        friend_username = self.cleaned_data.get("friend_username")
        friend = Account.objects.get(user_name=friend_username)

        if not user == friend:
            try:
                FriendshipRelation.objects.create(
                    user=user,
                    friend=friend
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


class AddRoomForm(forms.Form):
    chat_name = forms.CharField(max_length=30)
    def __init__(self, request, friends=None, *args, **kwargs):
        super(AddRoomForm, self).__init__(*args, **kwargs)
        if friends is None:
            aquired_friends_requests = set([
                relation.user for relation in
                FriendshipRelation.objects.filter(friend=request.user)
            ])
            # Set of users who were sent request by current user.
            send_friends_requests = set([
                relation.friend for relation in
                FriendshipRelation.objects.filter(user=request.user)
            ])
            # Set of users whoes requests has been accepted.
            friends = aquired_friends_requests.intersection(send_friends_requests)

        choice_list = [
            (friend.id, str(friend)) 
            for friend in friends
        ]

        self.fields['users'] = forms.MultipleChoiceField(
            choices=choice_list,
            required=True
        )

    @transaction.atomic
    def save(self, request):
        new_chatroom = ChatRoom.objects.create(
            name = self.cleaned_data.get("chat_name")
        )
        ChatRoomUsers.objects.create(
            chatroom = new_chatroom,
            user = get_object_or_404(Account, pk=request.user.id)
        )
        for user_id in self.cleaned_data.get("users"): # type: ignore
                ChatRoomUsers.objects.create(
                    chatroom = new_chatroom,
                    user = get_object_or_404(Account, pk=user_id)
                )
