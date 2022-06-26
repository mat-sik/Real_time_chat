from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages

from chat_app.forms import AddFriendForm, AddRoomForm
from chat_app.models import FriendshipRelation, ChatRoom, ChatRoomUsers


# Create your views here.
class ViewIndex(View):
    template_name = "chat_app/index.html"
    form_class_add_friend = AddFriendForm
    form_class_add_room = AddRoomForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form_add_friend = self.form_class_add_friend()

            # Set of users who sent request to current user.
            aquired_friends_requests = set([
                relation.user for relation in
                FriendshipRelation.objects.filter(friend=request.user)
            ])
            # Set of users who were sent request by current user.
            send_friends_requests = set([
                relation.friend for relation in
                FriendshipRelation.objects.filter(user=request.user)
            ])

            # Set of users whoes request hasn't been accepted yet.
            pending = aquired_friends_requests.difference(send_friends_requests)
            # Set of users whoes requests has been accepted.
            friends = aquired_friends_requests.intersection(send_friends_requests)

            form_add_room = self.form_class_add_room(request, friends)

            chatrooms_users = ChatRoomUsers.objects.filter(user=request.user)
            chatrooms = [i.chatroom for i in chatrooms_users]

            context = {
                "form_add_friend": form_add_friend,
                "form_add_room": form_add_room,
                "pending": pending,
                "friends": friends,
                "chatrooms": chatrooms
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
    form_class = AddRoomForm

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

                context = {"chatroom": chatroom}
                return render(request, self.template_name, context)

        messages.add_message(
            request, 
            messages.ERROR, 
            "You are not authorised."
        )

        return redirect("chat_app:index")