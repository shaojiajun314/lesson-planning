# -*- coding: utf-8 -*-
from django import forms
from django.forms import fields

from education.catalogue.models import Category

class CategoryCreateForm(forms.Form):
    name = fields.CharField(required=True, max_length=16)
    ancestor_id = fields.IntegerField(required=False)
    this_node_id = fields.IntegerField(required=False)

    ancestor_node = None
    this_node = None
    # image = fields.ImageField(required=True)

    def __init__(self, data, ancestor_id, this_node_id):
        self.ancestor_id = ancestor_id
        self.this_node_id = this_node_id
        super(CategoryCreateForm, self).__init__(data)

    def clean_ancestor_id(self):
        
        try:
            self.ancestor_node = Category.objects.get(
                id=self.cleaned_data['ancestor_id'])
        except Category.DoesNotExist:
            raise forms.ValidationError('上级分类不存在', 1011)

    def clean_this_node_id(self):


    def save(self):
        print self.cleaned_data
