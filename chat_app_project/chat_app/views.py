from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from account.forms import AccountCreationForm

# Create your views here.
class ViewRegister(View):
    form_class = AccountCreationForm
    template_name = "chat_app/register.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            form.save()
            new_user = authenticate(
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password1'),
            )
            login(request, new_user)
        else:
            context = {"form": form}
            return render(request, self.template_name, context)

        return redirect("chat_app:index")


class ViewLogin(View):
    form_class = AuthenticationForm
    template_name = "chat_app/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            login(request, user)
        else:
            context = {"form": form}
            return render(request, self.template_name, context)

        return redirect("chat_app:index")


class ViewLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("chat_app:login")


class ViewIndex(View):
    template_name = "chat_app/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return request