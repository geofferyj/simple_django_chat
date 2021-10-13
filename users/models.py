from django.db import models

# Create your models here.
from django.db.models.fields import EmailField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class User(AbstractUser):

    email = EmailField(_("Email"), blank=True, null=True, max_length=255)
