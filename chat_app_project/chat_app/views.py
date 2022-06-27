from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages

from chat_app.forms import AddFriendForm, AddChatRoomForm
from chat_app.models import FriendshipRelation, ChatRoom, ChatRoomUsers, Message
from account.models import Account


# Create your views here.
class ViewIndex(View):
    template_name = "chat_app/index.html"
    form_class_add_friend = AddFriendForm
    form_class_add_room = AddChatRoomForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Ids of users who were sent friend request by current user.
            sent_requests_uid = FriendshipRelation.objects.filter(
                user=request.user
            ).values("friend_id")

            # Ids of users who are friends with current user.
            friends_uid = FriendshipRelation.objects.filter(
                friend=request.user # aquired friend request of current user.
            ).filter(user_id__in=sent_requests_uid).values("user_id")

            # Ids of users who have pending friend request for current user.
            pending_uid = FriendshipRelation.objects.filter(
                friend=request.user
            ).exclude(user_id__in=sent_requests_uid).values("user_id")

            # Ids of users who were sent friend request by current user and
            # are not friends with current user. I want to reuse query.
            sent_uid = FriendshipRelation.objects.filter(
                user=request.user
            ).exclude(friend_id__in=friends_uid).values("friend_id")

            # Ids of chatrooms with current user.
            curr_user_cid = ChatRoomUsers.objects.filter(
                user_id=request.user
            ).values("chatroom_id")

            # Ids of private chatrooms with current user.
            curr_user_pcid = ChatRoom.objects.filter(
                id__in=curr_user_cid,
                is_private=True,
            ).values("id")

            # Nonprivate chatrooms with current user.
            curr_user_npc = ChatRoom.objects.filter(
                id__in=curr_user_cid,
                is_private=False,
            )

            # Private chatrooms with corresponding user who is a friend of current user.
            private_chatrooms_friends = ChatRoomUsers.objects.filter(
                chatroom_id__in=curr_user_pcid,
                user_id__in=friends_uid
            )
            # Private chatrooms with corresponding user who has sent
            # pending friend request to current user.
            private_chatrooms_pending = ChatRoomUsers.objects.filter(
                chatroom_id__in=curr_user_pcid,
                user_id__in=pending_uid
            )
            # Private chatrooms with corresponding user who is not friend with 
            # current user and was sent friend request by current user.
            private_chatrooms_sent = ChatRoomUsers.objects.filter(
                chatroom_id__in=curr_user_pcid
            ).filter(
                user_id__in=sent_uid
            )

            form_add_friend = self.form_class_add_friend()

            # Users who are friends with current user.
            friends=Account.objects.filter(
                id__in=friends_uid
            )
            form_add_room = self.form_class_add_room(request, friends)

            context = {
                "form_add_friend": form_add_friend,
                "form_add_room": form_add_room,
                "private_chatrooms_friends": private_chatrooms_friends,
                "private_chatrooms_pending": private_chatrooms_pending,
                "private_chatrooms_sent": private_chatrooms_sent,
                "nonprivate_chatrooms": curr_user_npc
            }
            return render(request, self.template_name, context)

        return redirect("chat_app:login")


class ViewAddFriend(View):
    template_name = "chat_app/index.html"
    form_class = AddFriendForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                if form.username_exists():
                    form.save(request)
                else:
                    messages.add_message(
                        request, 
                        messages.ERROR, 
                        "User does not exist."
                    )
            else:
                messages.add_message(
                    request, 
                    messages.ERROR, 
                    "Invalid data submited."
                )
        return redirect("chat_app:index")


class ViewAddChatRoom(View):
    form_class = AddChatRoomForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request, friends=None, data=request.POST)
            if form.is_valid():
                form.save(request)
            else:
                messages.add_message(
                    request, 
                    messages.ERROR, 
                    "Invalid data submited."
                )       
        return redirect("chat_app:index")


class ViewChatRoom(View):
    template_name = "chat_app/chatroom.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            chatroom = get_object_or_404(ChatRoom, pk=kwargs.get("chatroom_id"))
            chatroom_users = set([
                chatroom_user.user for chatroom_user in
                ChatRoomUsers.objects.filter(chatroom=chatroom)
            ])
            if request.user in chatroom_users:
                
                # Ordering by pub_date isn't required I think.
                chat_messages = Message.objects.filter(
                    chatroom=chatroom
                )

                context = {
                    "chatroom": chatroom,
                    "chat_messages": chat_messages,
                    }
                return render(request, self.template_name, context)

        messages.add_message(
            request, 
            messages.ERROR, 
            "You are not authorised."
        )

        return redirect("chat_app:index")