# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
def is_mobile_phone_number(value):
    if mobilephonenumber.match(value) is None:
        raise ValidationError(
            _('the string supplied did not seem to be '
              'a mobile phone number')
        )



# class UserManager(auth_models.BaseUserManager):
#
#     def create_user(self, mobile, password=None, **extra_fields):
#         """
#         Creates and saves a User with the given mobile phone number,
#         and password.
#         """
#         now = timezone.now()
#         if not mobile:
#             raise ValueError('The given mobile phone number must be set')
#         mobile = normalise_mobile(mobile)
#         user = self.model(
#             mobile=mobile, is_staff=False, is_active=True,
#             is_superuser=False,
#             last_login=now, date_joined=now, **extra_fields)
#
#         user.set_password(password)
#         user.save(using=self._db)
#         user.profile.create(
#             openid=uuid4().hex
#         )
#         return user
#
#     def create_superuser(self, mobile, password, **extra_fields):
#         u = self.create_user(mobile, password, **extra_fields)
#         u.is_staff = True
#         u.is_active = True
#         u.is_superuser = True
#         u.save(using=self._db)
#
#         u.profile.create(
#             openid=uuid4().hex
#         )
#
#
#         return u

class User(auth_models.AbstractBaseUser,
           auth_models.PermissionsMixin):
    username = models.CharField(
        max_length=64, unique=True)
    nickname = models.CharField(
        max_length=64, null=True, blank=True)
    mobile = models.CharField(
        _('mobile phone number'),
        max_length=64,
        validators=[is_mobile_phone_number],
        unique=True)
    email = models.EmailField(
        _('email address'), null=True, blank=True, unique=True)
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    # def get_full_name(self):
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()
    #
    # def get_short_name(self):
    #     return self.first_name