"""
Models for app dashboard
"""
import uuid  # Required for creating unique id for mentor/student session
from django.db import models
#  from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse


class UserManager(BaseUserManager):
    """
    Model for managing users
    """
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password and name.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a mentor(staff) user with the
        given email and password and name.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a course admin(superuser)
        with the given email and password and name.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Class for users (Mentors and Course admins)
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField('Mentor', default=False)
    admin = models.BooleanField('Course manager', default=False)
    name = models.CharField('First Name', max_length=80, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Username is set to email
    REQUIRED_FIELDS = []  # Email and Password are required fields

    def get_full_name(self):
        """
        User is identified by email
        """
        return self.email

    def get_short_name(self):
        """
        The user is identified by their email address
        """
        return self.email

    def __str__(self):
        """
        Return email as string
        """
        return str(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

