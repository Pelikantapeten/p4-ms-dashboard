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