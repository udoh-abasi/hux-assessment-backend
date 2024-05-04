from django.contrib import admin
from .models import Contact


# Fields we want to display on the /admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ("firstName", "lastName", "phoneNumber", "user", "dateAdded")


admin.site.register(Contact, UserAdmin)
