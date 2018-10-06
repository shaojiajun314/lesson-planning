#!coding:utf-8
from django import forms
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from education.education_user.models import is_mobile_phone_number
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
                raise forms.ValidationError('帐号或者密码错误', 1010)
            self.user = user
            return self.cleaned_data

class UserCreateForm(forms.Form):

    username = forms.fields.CharField(required=True, min_length=8, max_length=16)
    password = forms.fields.CharField(required=True, min_length=8, max_length=32)
    mobile = forms.fields.CharField(required=True, min_length=11, max_length=16)
    email = forms.EmailField(required=False)
    nickname = forms.fields.CharField(required=False, max_length=10)

    def clean_username(self):
        user = User.objects.filter(username=self.cleaned_data['username'])
        if user:
            raise forms.ValidationError('用户已注册', 1012)
        return self.cleaned_data['username']

    def clean_mobile(self):
        try:
            is_mobile_phone_number(self.cleaned_data['mobile'])
        except:
            raise forms.ValidationError('手机号不合法', 1013)
        user = User.objects.filter(mobile=self.cleaned_data['mobile'])
        if user:
            raise forms.ValidationError('该手机用户已经注册', 1012)
        return self.cleaned_data['mobile']

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if user:
            raise forms.ValidationError('该邮箱用户已经注册', 1014)
        return self.cleaned_data['email']

    def save(self):
        data = {
            'mobile': self.cleaned_data['mobile'],
            'email': self.cleaned_data['email'],
            'nickname': self.cleaned_data['nickname']
        }
        return User.objects.create_user(self.cleaned_data['username'],
            password=self.cleaned_data['password'], **data)
