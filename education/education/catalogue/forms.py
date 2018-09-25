# -*- coding: utf-8 -*-
from django import forms
from django.forms import fields


class ExampleCreateForm(forms.Form):

    categories
    content


    store_bonus_ratio = fields.IntegerField(required=True)
    consume_bonus_ratio = fields.IntegerField(required=True)
    share_bonus_ratio = fields.IntegerField(required=True)
    leader_bonus_ratio = fields.IntegerField(required=True)
    product_recommend_bonus_ratio = fields.IntegerField(required=True)
    company_management_bonus_ratio = fields.IntegerField(required=True)
    company_risk_reserve_ratio = fields.IntegerField(required=True)
    platform_profit = fields.IntegerField(required=True)


    def __init__(self, )

    def clean(self):
        clean_data = self.cleaned_data
        keys = clean_data.keys()
        assert keys == 8 #9
        total_ratio = 0
        for key in keys:
            clean_data[key] = int(clean_data[key])
            total_ratio = total_ratio + clean_data[key]
        assert total_ratio == 100

    def save(self):
        new_setting = Setting()
        new_setting.update_setting(**self.cleaned_data)
