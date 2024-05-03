from django.contrib import admin
from .models import AppUser


class UserAdmin(admin.ModelAdmin):
    list_display = ("email",)


admin.site.register(AppUser, UserAdmin)
