# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _

import re
# Create your models here.

mobilephonenumber = re.compile((
    r'^(\+?(?:0086|086|86))?((?:13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[013567'
    r'8]|18[0-9]|19[89])(?:\d{8}))$'))
def is_mobile_phone_number(value):
    if mobilephonenumber.match(value) is None:
        raise ValidationError(
            _('the string supplied did not seem to be '
              'a mobile phone number')
        )


class UserManager(auth_models.BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given mobile phone number,
        and password.
        """
        now = timezone.now()
        user = self.model(
            username=username, is_staff=False, is_active=True,
            is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(username, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class User(auth_models.AbstractBaseUser,
           auth_models.PermissionsMixin):
    username = models.CharField(
        max_length=16, unique=True)
    password = models.CharField(_('password'),
        max_length=32)
    nickname = models.CharField(
        max_length=10, null=True, blank=True)
    mobile = models.CharField(
        _('mobile phone number'),
        max_length=11,
        validators=[is_mobile_phone_number],
        null=True,
        unique=True)
    email = models.EmailField(
        _('email address'),
        null=True,
        blank=True)

    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(_('last login'),
        default=timezone.now)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'user'

    # def get_full_name(self):
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()
    #
    # def get_short_name(self):
    #     return self.first_name
