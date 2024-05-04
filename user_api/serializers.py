from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

    # This will create the user
    def create(self, clean_data):
        user_obj = User.objects.create_user(
            email=clean_data["email"], password=clean_data["password"]
        )

        # Then save the created user
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        # Authenticate user against the database
        user = authenticate(
            username=clean_data["email"], password=clean_data["password"]
        )

        if not user:
            raise ValidationError("User not found")
        return user


# This ensures that the email and id is sent to the frontend
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")
