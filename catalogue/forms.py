# -*- coding: utf-8 -*-
#django
from django import forms
from django.forms import fields
from django.db import transaction

#apps
from education.catalogue.models import Category, Example

class BaseMultiImagesForm(forms.Form):
    def add_image_field(self, field_name):
        self.fields[field_name] = fields.ImageField(required=True)

class CategoryCreateForm(forms.Form):
    name = fields.CharField(required=True, max_length=16)
    img = fields.ImageField(required=False)
    # ancestor_id = fields.IntegerField(required=False)

    ancestor_node = None
    # image = fields.ImageField(required=True)

    def __init__(self, data, file, ancestor_id):
        self.ancestor_id = ancestor_id
        super(CategoryCreateForm, self).__init__(data, files=file)

    def clean(self):
        if self.ancestor_id:
            try:
                self.ancestor_node = Category.objects.get(
                    id=self.ancestor_id)
            except Category.DoesNotExist:
                raise forms.ValidationError('上级分类不存在', 1011)
        return self.cleaned_data

    def save(self):
        image_name = None
        if self.cleaned_data['img']:
            image_name = self.cleaned_data['img'].name
        agrs = {
            'name': self.cleaned_data['name'],
            'image_name': image_name,
            'image': self.cleaned_data['img']
        }
        if not self.ancestor_node:
            return Category.add_root(**agrs)
        return self.ancestor_node.add_child(**agrs)

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

class ExampleCreateForm(BaseMultiImagesForm):
    category_id = fields.IntegerField(required=True)
    content = fields.CharField(required=True, max_length=512)
    answer = fields.CharField(required=True, max_length=512)

    def __init__(self, data, files):
        super(ExampleCreateForm, self).__init__(data, files=files)
        for file_name in files:
            self.add_image_field(file_name)

    def clean_category_id(self):
        try:
            self.category = Category.objects.get(id=self.cleaned_data['category_id'])
        except Category.DoesNotExist:
            raise forms.ValidationError('该分类不存在', 1011)
        return self.cleaned_data['category_id']

    def save(self):
        with transaction.atomic():
            example = self.category.examples.create(
                content=self.cleaned_data['content']
            )
            for k, v in self.cleaned_data.items():
                if k.startswith('content_img'):
                    example.images.create(
                        image=v,
                        image_name=v.name
                    )

            ans = example.answers.create(
                answer=self.cleaned_data['answer']
            )
            for k, v in self.cleaned_data.items():
                if k.startswith('answer_img'):
                    ans.images.create(
                        image=v,
                        image_name=v.name
                    )

            return example

class ExampleUpdateForm(BaseMultiImagesForm):
    content = fields.CharField(required=True, max_length=512)

    def __init__(self, data, this_example_id):
        self.this_example_id = this_example_id
        super(ExampleUpdateForm, self).__init__(data)

    def clean(self):
        try:
            self.this_example = Example.objects.get(
                id=self.this_example_id)
        except Example.DoesNotExist:
            raise forms.ValidationError('该题目不存在', 1011)

        return self.cleaned_data


    def save(self):
        self.this_example.content = self.cleaned_data['content']
        self.this_example.save()
        return self.this_example
