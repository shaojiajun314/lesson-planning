# -*- coding: utf-8 -*-
from django import forms
from django.forms import fields

from education.catalogue.models import Category

class CategoryCreateForm(forms.Form):
    name = fields.CharField(required=True, max_length=16)
    # ancestor_id = fields.IntegerField(required=False)

    ancestor_node = None
    # image = fields.ImageField(required=True)

    def __init__(self, data, ancestor_id):
        print ancestor_id
        self.ancestor_id = ancestor_id
        super(CategoryCreateForm, self).__init__(data)

    def clean(self):
        if self.ancestor_id:
            try:
                self.ancestor_node = Category.objects.get(
                    id=self.ancestor_id)
            except Category.DoesNotExist:
                raise forms.ValidationError('上级分类不存在', 1011)
        return self.cleaned_data

    def save(self):
        if not self.ancestor_node:
            print self.cleaned_data
            return Category.add_root(**{
                'name': self.cleaned_data['name']
            })
        return self.ancestor_node.add_child(**{
                'name': self.cleaned_data['name']
            })
            # print dir(Category)

class CategoryUpdateForm(forms.Form):
    name = fields.CharField(required=True, max_length=16)
    # this_node_id = fields.IntegerField(required=True)

    this_node = None
    # image = fields.ImageField(required=True)

    def __init__(self, data, this_node_id):
        self.this_node_id = this_node_id
        super(CategoryUpdateForm, self).__init__(data)

    def clean(self):
        try:
            self.this_node = Category.objects.get(
                id=self.this_node_id)
        except Category.DoesNotExist:
            raise forms.ValidationError('该分类不存在', 1011)

        return self.cleaned_data


    def save(self):
        self.this_node.name = self.cleaned_data['name']
        self.this_node.save()
        return self.this_node
