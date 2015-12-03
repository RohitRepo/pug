import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.slugger import unique_slugify

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(verbose_name='name', max_length=80)
    slug = models.SlugField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True,)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        self.email = self.normalize_email(self.email)
        super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """

        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            raise Exception(
                "Invalid email id recieved during mormalization %s" % (ValueError))
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email
