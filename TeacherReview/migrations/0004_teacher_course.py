# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherReview', '0003_auto_20171001_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='course',
            field=models.CharField(default=' ', max_length=500),
            preserve_default=False,
        ),
    ]
