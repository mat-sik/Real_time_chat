from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

# Register your models here.
class UserAdminConfig(UserAdmin):
    ordering = ("-date_joined",)
    search_fields = ("email", "user_name")
    list_filter = (
        "email", "user_name", "is_active", "is_staff", "is_superuser" 
    )
    list_display = (
        "email", "user_name", "is_active", "is_staff", "is_superuser"
    )
    readonly_fields = ("id", "date_joined", "last_login")
    fieldsets = ()

admin.site.register(Account, UserAdminConfig)