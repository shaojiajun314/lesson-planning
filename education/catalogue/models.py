# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from treebeard.mp_tree import MP_Node
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from education.education_user.models import User
from education.db.models.fields import EDUImageField, EDUFileField
# Create your models here.

class Category(MP_Node):
    name = models.CharField(_('Name'),
        max_length=64)
    image = EDUImageField(_('Image'),
        upload_to='images/categories',
        blank=True,
        null=True,
        max_length=255)
    image_name = models.CharField(_('Image Name'),
        max_length=64,
        blank=True,
        null=True,)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = (
            ("modify_category", "Can modify a category"),
        )



class Example(models.Model):
    categories = models.ManyToManyField(
        Category,
        related_name='examples')
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    difficulty = models.FloatField(default=0)

    class Meta:
        permissions = (
            ("modify_example", "Can modify a example"),
        )

    # def get_analytics(self):
    #     try:
    #         return self.analytics
    #     except:
    #         return ExampleRecord.objects.create(
    #             example=self
    #         )


class ExampleImage(models.Model):
    example = models.ForeignKey(
        Example,
        on_delete=models.CASCADE,
        related_name='images',)

    image = EDUImageField(_('Image'),
        upload_to='images/example',
        blank=True,
        null=True,
        max_length=255)
    image_name = models.CharField(_('Image Name'),
        max_length=64,
        blank=True,
        null=True,)
    date_created = models.DateTimeField(default=timezone.now)


class Answer(models.Model):
    example = models.ForeignKey(
        Example,
        on_delete=models.CASCADE,
        related_name='answers',)
    answer = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    # image = EDUImageField(_('Image'),
    #     upload_to='categories',
    #     blank=True,
    #     null=True,
    #     max_length=255)
    # image_name = models.CharField(_('Image Name'), max_length=64)

class AnswerImage(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='images',)

    image = EDUImageField(_('Image'),
        upload_to='images/example',
        blank=True,
        null=True,
        max_length=255)
    image_name = models.CharField(_('Image Name'),
        max_length=64,
        blank=True,
        null=True,)
    date_created = models.DateTimeField(default=timezone.now)


class EDUFile(models.Model):
    categories = models.ManyToManyField(
        Category,
        related_name='files')
    date_created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=16, null=True, blank=True)
    # courseware, examination_outline

    file = EDUFileField(
        upload_to='files/EDUFile',
        blank=True,
        null=True,
        max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='files',)

    class Meta:
        permissions = (
            ("modify_edufile", "Can modify a modify_edufile"),
        )

# class CourseWare(models.Model):
#     categories = models.ManyToManyField(
#         Category,
#         related_name='courseware')
#     date_created = models.DateTimeField(default=timezone.now)
#     title = models.CharField(max_length=64, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     file = EDUFileField(
#         upload_to='files/courseware',
#         blank=True,
#         null=True,
#         max_length=255)
#     user = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='courseware',)
#
#     class Meta:
#         permissions = (
#             ("modify_courseware", "Can modify a modify_courseware"),
#         )
#
# class ExaminationOutline(models.Model):
#     categories = models.ManyToManyField(
#         Category,
#         related_name='examination_outline')
#     date_created = models.DateTimeField(default=timezone.now)
#     title = models.CharField(max_length=64, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     file = EDUFileField(
#         upload_to='files/examination_outline',
#         blank=True,
#         null=True,
#         max_length=255)
#     user = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='examination_outline',)
#
#     class Meta:
#         permissions = (
#             ("modify_examinationoutline", "Can modify a examinationoutline"),
#         )
