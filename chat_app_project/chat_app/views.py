from django.shortcuts import render
from django.views import View

# Create your views here.
class ViewIndex(View):
    template_name = "chat_app/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return request


class ViewRoom(View):
    template_name = "chat_app/chatroom.html"

    def get(self, request, *args, **kwargs):
        context = {"room_name": kwargs.get("room_name")}

        return render(request, self.template_name, context)