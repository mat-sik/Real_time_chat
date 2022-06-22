from django.contrib.auth.forms import UserCreationForm

from chat_app.models import Account

class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ("email", "user_name")