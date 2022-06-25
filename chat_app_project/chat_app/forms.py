from django import forms
from django.db.utils import IntegrityError
from django.contrib import messages

from account.models import Account
from chat_app.models import FriendshipRelation


class AddFriendForm(forms.Form):
    friend_username = forms.CharField(max_length=30)

    def username_exists(self):
        friend_username = self.data.get("friend_username")
        return Account.objects.filter(user_name=friend_username).count() > 0

    def save(self, request):
        user = request.user
        friend_username = self.data.get("friend_username")
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
