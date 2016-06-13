import os
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from contact_share_service.managers import CustomUserManager
from contact_share.settings import AUTH_USER_MODEL


@receiver(post_save, sender=AUTH_USER_MODEL)
def finalize_account_creation(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

    if created and not instance.is_admin:
        instance.set_password(instance.password)
        instance.save()


def get_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    name = str(uuid.uuid4()).replace('-', '_')
    filename = '{}.{}'.format(name, ext)
    return os.path.join('images', filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, blank=False, unique=True)
    full_name = models.CharField(max_length=255, blank=False)

    password_reset_key = models.IntegerField(blank=False, default=-1)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Card(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    job_title = models.CharField(max_length=255, blank=False)
    contact_number = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    organization = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=get_image_file_path)
