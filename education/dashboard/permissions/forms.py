# -*- coding: utf-8 -*-
from json import loads

#django
from django import forms
from django.forms import fields
from django.contrib.auth.models import Permission

#apps
from education.education_user.models import User

# UserPermissonDeleteForm
# UserPermissonCreateForm
class UserPermissonCreateForm(forms.Form):
    username = fields.CharField(required=True, max_length=16)
    codename = fields.CharField(required=True, max_length=63)

    def clean_username(self):
        try:
            print self.cleaned_data['username']
            self.user = User.objects.get(
                username=self.cleaned_data['username'])
        except User.DoesNotExist:
            raise forms.ValidationError('该用户不存在', 1011)
        return self.cleaned_data['username']

    def clean_codename(self):
        try:
            self.permission = Permission.objects.get(
                codename=self.cleaned_data['codename'])
        except Permission.DoesNotExist:
            raise forms.ValidationError('该权限不存在', 1011)
        return self.cleaned_data['codename']

    def save(self):
        self.user.user_permissions.add(self.permission)
        return self.user

class UserPermissonDeleteForm(forms.Form):
    codename = fields.CharField(required=True, max_length=63)

    def __init__(self, data, username):
        self.username = username
        super(UserPermissonDeleteForm, self).__init__(data)

    def clean_codename(self):
        try:
            self.permission = Permission.objects.get(
                codename=self.cleaned_data['codename'])
        except Permission.DoesNotExist:
            raise forms.ValidationError('该权限不存在', 1011)
        return self.cleaned_data['codename']

    def clean(self):
        try:
            self.user = User.objects.get(
                username=self.username)
        except User.DoesNotExist:
            raise forms.ValidationError('该用户不存在', 1011)

        if not User.objects.filter(user_permissions=self.permission, id=self.user.id):
            raise forms.ValidationError('该用户没有此权限', 1012)
        return self.cleaned_data

    def save(self):
        self.user.user_permissions.remove(self.permission)
        return self.user
