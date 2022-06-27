from account.models import Account

for i in range(10):
    Account.objects.create_user( # type: ignore
        email=f"test{i}@gmail.com",
        username=f"test{i}",
        password=f"1234"
    )
