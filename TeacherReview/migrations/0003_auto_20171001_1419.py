# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-01 14:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherReview', '0002_auto_20171001_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='ques_no',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='teacher_class_id',
            new_name='teacher',
        ),
    ]
