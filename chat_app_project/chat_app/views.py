from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from chat_app.forms import AddFriendForm, AddRoomForm
from chat_app.models import FriendshipRelation
from account.models import Account

# Create your views here.
class ViewIndex(View):
    template_name = "chat_app/index.html"
    form_class_add_friend = AddFriendForm
    form_class_add_room = AddRoomForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # aquired_friends_requests = FriendshipRelation.objects.filter(friend=request.user)
            # send_friends_requests = FriendshipRelation.objects.filter(user=request.user)
            
            # asked_users = set([i.friend for i in send_friends_requests])
            # pending = aquired_friends_requests.exclude(user__in=asked_users)
            # friends = aquired_friends_requests.filter(user__in=asked_users)
            
            # friend_users = Account.objects.filter(id__in=set(i.user.id for i in friends))
            # pending_users = Account.objects.filter(id__in=set(i.user.id for i in pending))


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

            context = {
                "form_add_friend": form_add_friend,
                "form_add_room": form_add_room,
                "pending": pending,
                "friends": friends
            }
            return render(request, self.template_name, context)
        else:
            return redirect("chat_app:login")

    def post(self, request, *args, **kwargs):
        return request


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
        else:
            return redirect("chat_app:login")


class ViewAddRoom(View):
    form_class = AddRoomForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request, friends=None, data=request.POST)
            if form.is_valid():
                form.save()
            else:
                messages.add_message(
                        request, 
                        messages.ERROR, 
                        "Invalid data submited."
                    )       
            return redirect("chat_app:index")
        else:
            return redirect("chat_app:login")


class ViewRoom(View):
    template_name = "chat_app/chatroom.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {"room_name": kwargs.get("room_name")}

            return render(request, self.template_name, context)
        else:
            return redirect("chat_app:login")