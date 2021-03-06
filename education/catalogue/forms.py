# -*- coding: utf-8 -*-
from json import loads

#django
from django import forms
from django.forms import fields
from django.conf import settings
from django.db import transaction

#apps
from education.analytics.models import ExampleRecord
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
    img = fields.ImageField(required=False)

    this_node = None

    def __init__(self, data, files, this_node_id):
        self.this_node_id = this_node_id
        super(CategoryUpdateForm, self).__init__(data, files=files)

    def clean(self):
        try:
            self.this_node = Category.objects.get(
                id=self.this_node_id)
        except Category.DoesNotExist:
            raise forms.ValidationError('该分类不存在', 1011)

        return self.cleaned_data

    def save(self):
        if self.this_node.name == self.cleaned_data['name'] and \
            (not self.cleaned_data['img']):
            return self.this_node
        self.this_node.name = self.cleaned_data['name']
        if self.cleaned_data['img']:
            self.this_node.image = self.cleaned_data['img']
            self.this_node.image_name = self.cleaned_data['img'].name
        self.this_node.save()
        return self.this_node
        # self.this_node.name = self.cleaned_data['name']
        # self.this_node.save()
        # return self.this_node

class ExampleCreateForm(EDUBaseForm):
    category_id = fields.IntegerField(required=True)
    content = fields.CharField(required=True, max_length=512)
    answer = fields.CharField(required=True, max_length=512)
    difficulty = fields.FloatField(required=True)

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

    def clean_difficulty(self):
        if self.cleaned_data['difficulty'] < 0 or \
            self.cleaned_data['difficulty'] > 1:
            raise forms.ValidationError('难度系数不合法', 1012)
        return self.cleaned_data['difficulty']

    def save(self):
        with transaction.atomic():
            example = self.category.examples.create(
                content=self.cleaned_data['content'],
                difficulty=self.cleaned_data['difficulty'],
            )
            ExampleRecord.objects.create(
                example=example
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
    difficulty = fields.FloatField(required=True)

    answer_delete_list = []
    example_imgs_delete_list = []

    def __init__(self, data, this_example_id, files):
        super(ExampleUpdateForm, self).__init__(data, files=files)
        self.this_example_id = this_example_id
        for file_name in files:
            self.add_image_field(file_name)

    def clean_category_id(self):
        try:
            self.category = Category.objects.get(id=self.cleaned_data['category_id'])
        except Category.DoesNotExist:
            raise forms.ValidationError('该分类不存在', 1011)
        return self.cleaned_data['category_id']

    def clean_difficulty(self):
        if self.cleaned_data['difficulty'] < 0 or \
            self.cleaned_data['difficulty'] > 1:
            raise forms.ValidationError('难度系数不合法', 1012)
        return self.cleaned_data['difficulty']


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

            self.example_imgs_delete_list = \
                self.this_example.images.filter(id__in=example_imgs_list)
        except:
            raise forms.ValidationError('example_imgs_delete 参数错误', 1019)

        return self.cleaned_data

    def update_categories(self):
        for cate in self.this_example.categories.all():
            self.this_example.categories.clear()
        self.this_example.categories.add(self.category)
        for cate in self.category.get_ancestors():
            self.this_example.categories.add(cate)

    def save(self):
        with transaction.atomic():
            self.update_categories()
            self.answer_delete_list.delete()
            self.example_imgs_delete_list.delete()
            self.this_example.content = self.cleaned_data['content']
            self.this_example.difficulty = self.cleaned_data['difficulty']
            for k, v in self.cleaned_data.items():
                if k.startswith('content_img'):
                    self.this_example.images.create(
                        image=v,
                        image_name=v.name
                    )
            print self.cleaned_data['answer'],1238713819837
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
            self.this_example.save()
            return self.this_example

class FileCreateForm(forms.Form):
    category_id = fields.IntegerField(required=True)
    title = fields.CharField(required=True, max_length=64)
    description = fields.CharField(required=True, max_length=512)
    file = fields.FileField(required=False)

    def __init__(self, data, files, type_):
        super(FileCreateForm, self).__init__(data, files=files)
        self.type = type_

    def clean_category_id(self):
        try:
            self.category = Category.objects.get(id=self.cleaned_data['category_id'])
        except Category.DoesNotExist:
            raise forms.ValidationError('该分类不存在', 1011)
        return self.cleaned_data['category_id']

    def clean(self):
        if self.type not in settings.EDUFILE_TYPE_LIST:
            raise forms.ValidationError('type-error', 1012)
        return self.cleaned_data

    def save(self, user):
        f_c = self.category.files.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            file=self.cleaned_data['file'],
            user=user,
            type=self.type
        )

        for cate in self.category.get_ancestors():
            f_c.categories.add(cate)

        return f_c



# FileDeleteForm
# FileCreateForm
