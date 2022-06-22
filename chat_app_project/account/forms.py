from django.contrib.auth.forms import UserCreationForm

from account.models import Account

class AccountCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ("email", "user_name",)