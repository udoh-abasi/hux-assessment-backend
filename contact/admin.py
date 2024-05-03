from django.contrib import admin
from .models import Contact


class UserAdmin(admin.ModelAdmin):
    list_display = ("firstName", "lastName", "phoneNumber", "user", "dateAdded")


admin.site.register(Contact, UserAdmin)
