#!coding:utf-8
from django import forms
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.fields.CharField(required=True, min_length=8, max_length=16)
    password = forms.fields.CharField(required=True, min_length=8, max_length=32)

    def clean(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            raise forms.ValidationError('帐号号未注册', 1011)
        else:
            user = authenticate(username=self.cleaned_data['username'],
                                password=self.cleaned_data['password'])
            if user == None:
                raise forms.ValidationError('手机号或者密码错误', 1010)
            self.user = user
            return self.cleaned_data

class UserCreateForm(forms.Form):

    username = forms.fields.CharField(required=True, min_length=8, max_length=16)
    password = forms.fields.CharField(required=True, min_length=8, max_length=32)

    def clean_username(self):
        user = User.objects.filter(username=self.cleaned_data['username'])
        if user:
            raise forms.ValidationError('手机号已注册', 1012)
        return self.cleaned_data['username']

    def save(self):
        return User.objects.create_user(self.cleaned_data['username'],
            password=self.cleaned_data['password'])
