from account.models import Account

for i in range(10):
    Account.objects.create_user( # type: ignore
        email=f"user{i}@gmail.com",
        username=f"user{i}",
        password=f"1234"
    )
