from rest_framework import serializers
from .views import Contact


# This serialize the contact object and return all the fields to the frontend
class AllContacts(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
