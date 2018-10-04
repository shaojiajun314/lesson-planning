# -*- coding: utf-8 -*-
#django
from django import forms
from django.forms import fields
from django.db import transaction

#apps
from education.catalogue.models import Category, Example

class EDUBaseForm(forms.Form):
    def add_image_field(self, field_name):
        self.fields[field_name] = fields.ImageField(required=True)

    def add_char_field(self, field_name, max_length):
        self.fields[field_name] = fields.CharField(required=True,
            max_length=max_length)

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

class ExampleCreateForm(EDUBaseForm):
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
            for cate in self.category.get_ancestors():
                example.categories.add(cate)
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

class ExampleUpdateForm(EDUBaseForm):
    category_id = fields.IntegerField(required=True)
    content = fields.CharField(required=True, max_length=512)
    answer = fields.CharField(required=False, max_length=512)

    example_imgs_delete = fields.CharField(required=False, max_length=512) #json
    answer_delete = fields.CharField(required=False, max_length=512) #json

    answer_delete_list = []

    def __init__(self, data, this_example_id, files):
        super(ExampleUpdateForm, self).__init__(data)
        self.this_example_id = this_example_id
        for file_name in files:
            self.add_image_field(file_name)

    def clean_category_id(self):
        try:
            self.category = Category.objects.get(id=self.cleaned_data['category_id'])
        except Category.DoesNotExist:
            raise forms.ValidationError('该分类不存在', 1011)
        return self.cleaned_data['category_id']


    def clean(self):
        try:
            self.this_example = Example.objects.get(
                id=self.this_example_id)
        except Example.DoesNotExist:
            raise forms.ValidationError('该题目不存在', 1011)

        try:
            answer_list = loads(self.cleaned_data['answer_delete'])
            self.answer_delete_list = \
                self.this_example.answers.filter(id__in=answer_list)
        except:
            raise forms.ValidationError('answer_delete 参数错误', 1019)

        try:
            example_imgs_list = loads(self.cleaned_data['example_imgs_delete'])
            self.example_imgs_delete = \
                self.this_example.images.filter(id__in=example_imgs_list)
        except:
            raise forms.ValidationError('answer_delete 参数错误', 1019)

        return self.cleaned_data

    def update_categories(self):
        for cate in self.this_example.categories.all():
            self.this_example.remove(cate)
        self.categories.add(self.category)
        for cate in self.category.get_ancestors():
            self.this_example.categories.add(cate)

    def save(self):
        with transaction.atomic():
            self.update_categories()
            self.answer_delete_list.delete()
            self.example_imgs_delete.delete()
            self.this_example.content = self.cleaned_data['content']
            for k, v in self.cleaned_data.items():
                if k.startswith('content_img'):
                    self.this_example.images.create(
                        image=v,
                        image_name=v.name
                    )
            if self.cleaned_data['answer']:
                ans = self.this_example.answers.create(
                    answer=self.cleaned_data['answer']
                )
                for k, v in self.cleaned_data.items():
                    if k.startswith('answer_img'):
                        ans.images.create(
                            image=v,
                            image_name=v.name
                        )
            return self.this_example
