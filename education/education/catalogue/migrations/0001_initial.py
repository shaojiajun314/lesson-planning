# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-23 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import education.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('image', education.db.models.fields.EDUImageField(blank=True, max_length=255, null=True, upload_to='categories', verbose_name='Image')),
                ('image_name', models.CharField(max_length=64, verbose_name='Image Name')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', education.db.models.fields.EDUImageField(blank=True, max_length=255, null=True, upload_to='example', verbose_name='Image')),
                ('image_name', models.CharField(max_length=64, verbose_name='Image Name')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalogue.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('image', education.db.models.fields.EDUImageField(blank=True, max_length=255, null=True, upload_to='categories', verbose_name='Image')),
                ('image_name', models.CharField(max_length=64, verbose_name='Image Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('categories', models.ManyToManyField(related_name='examples', to='catalogue.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ExampleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', education.db.models.fields.EDUImageField(blank=True, max_length=255, null=True, upload_to='example', verbose_name='Image')),
                ('image_name', models.CharField(max_length=64, verbose_name='Image Name')),
                ('example', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalogue.Example')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='example',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='catalogue.Example'),
        ),
    ]
