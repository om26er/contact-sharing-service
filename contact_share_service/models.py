import os
import uuid

from django.db import models

from rest_framework.authtoken.models import Token
from simple_login.models import BaseUser

from contact_share.settings import AUTH_USER_MODEL


def get_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    name = str(uuid.uuid4()).replace('-', '_')
    filename = '{}.{}'.format(name, ext)
    return os.path.join('images', filename)


class User(BaseUser):
    full_name = models.CharField(max_length=255, blank=False)


class Card(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    job_title = models.CharField(max_length=255, blank=False)
    contact_number = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    organization = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=get_image_file_path, blank=True)
    logo = models.ImageField(upload_to=get_image_file_path, blank=True)
    is_image = models.BooleanField(blank=False, default=False)
    design = models.IntegerField(default=-1)
