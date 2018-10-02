# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from treebeard.mp_tree import MP_Node
from django.db import models
from django.utils.translation import ugettext_lazy as _

from education.db.models.fields import EDUImageField

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


class Example(models.Model):
    categories = models.ManyToManyField(
        Category,
        related_name='examples')
    content = models.TextField()

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

class Answer(models.Model):
    example = models.ForeignKey(
        Example,
        on_delete=models.CASCADE,
        related_name='answers',)
    answer = models.TextField()

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
