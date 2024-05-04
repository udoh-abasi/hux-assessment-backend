from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid


# So, we want to use a custom user model, and not the default that comes with django
class AppUserManager(BaseUserManager):
    # This function will run to create a user, and save in the database.
    def create_user(self, email, password=None, **other_fields):
        if email is None:
            raise ValueError("An email is required")

        if password is None:
            raise ValueError("A password is required")

        email = self.normalize_email(email)
        user = self.model(email=email)

        # The hashed password will be saved
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        # To create a superuser (that can log in to the admin panel), this function will run
        if email is None:
            raise ValueError("An email is required")

        if password is None:
            raise ValueError("A password is required")

        user = self.create_user(email, password)

        # After creating a user, we just specify that we want them to be a superuser and have all the privileges (like logging in to the django admin panel)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(max_length=1, default=False)

    date_joined = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    objects = AppUserManager()
