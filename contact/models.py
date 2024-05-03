from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    firstName = models.CharField(max_length=999, null=False, blank=False)
    lastName = models.CharField(max_length=999, null=False, blank=False)
    phoneNumber = models.CharField(max_length=999, null=False, blank=False)
    dateAdded = models.DateTimeField(auto_now_add=True)
