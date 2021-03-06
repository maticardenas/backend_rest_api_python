from typing import Optional, TYPE_CHECKING

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class UserProfileManager(BaseUserManager):
    """
        Manager for user profiles
        This is required as otherwise Django will look for the default User model
        by default
    """

    def create_user(self, email: str, name: str, password: Optional[str] = None) -> "User":
        """Create a new user profile"""
        if not email:
            raise ValueError("Users must have an email address")

        # First part of an email could be case sensitive, but second should be lower case,
        # that's why normalize is required, to make the second part lower case.
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        # if we don't support multiple data bases the argument can be ommited.
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, name: str, password: str) -> "User":
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self) -> str:
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self) -> str:
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


class ProfileFeedItem(models.Model):
    """ Profile status update """
    # This way we ensure if we change our authorization user model, there won't be need of updating here the reference
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status_text = models.CharField(max_length=255)
    # Automatically we set to the current date
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status_text