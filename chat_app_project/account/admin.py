from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

# Register your models here.
class UserAdminConfig(UserAdmin):
    ordering = ("-date_joined",)
    search_fields = ("email", "username")
    list_filter = (
        "email", "username", "is_active", "is_staff", "is_superuser" 
    )
    list_display = (
        "email", "username", "is_active", "is_staff", "is_superuser"
    )
    readonly_fields = ("id", "date_joined", "last_login")
    fieldsets = ()

admin.site.register(Account, UserAdminConfig)