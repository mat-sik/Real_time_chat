from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from account.forms import AccountCreationForm, CustomAuthenticationForm

# Create your views here.
class ViewRegister(View):
    form_class = AccountCreationForm
    template_name = "account/register.html"

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
            messages.add_message(
                request, 
                messages.INFO, 
                "Registration successful, you are logged in."
            )
            return redirect("chat_app:index")

        messages.add_message(
            request, 
            messages.ERROR, 
            "Registration unsuccessful, try again."
        )

        context = {"form": form}
        return render(request, self.template_name, context)


class ViewLogin(View):
    form_class = CustomAuthenticationForm
    template_name = "account/login.html"

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
            messages.add_message(
                request, 
                messages.INFO, 
                "Login successful."
            )
            return redirect("chat_app:index")

        messages.add_message(
            request, 
            messages.ERROR, 
            "Login unsuccessful, try again."
        )

        context = {"form": form}
        return render(request, self.template_name, context)


class ViewLogout(View):
    def get(self, request, *args, **kwargs):
        messages.add_message(
            request, 
            messages.INFO, 
            "Logout successful."
        )

        logout(request)
        return redirect("chat_app:login")