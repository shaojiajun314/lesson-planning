# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from education.catalogue.models import Example
# Create your models here.

class ExampleRecord(models.Model):
    example = models.OneToOneField(
        Example,
        on_delete=models.CASCADE,
        related_name='analytics',)
    num_assemble = models.PositiveIntegerField(default=0)
