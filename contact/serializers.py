from rest_framework import serializers
from .views import Contact


class AllContacts(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
