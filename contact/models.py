from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Contact(models.Model):
    # Every contact should be associated to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    firstName = models.CharField(max_length=999, null=False, blank=False)
    lastName = models.CharField(max_length=999, null=False, blank=False)
    phoneNumber = models.CharField(max_length=999, null=False, blank=False)

    # The date field was added so we can know when the user created the contact, and sort result based on the date the contact was added
    dateAdded = models.DateTimeField(auto_now_add=True)
