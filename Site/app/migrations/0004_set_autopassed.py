# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_recordfuzzymatch'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='AutoPassed',
            field=models.NullBooleanField(),
        ),
    ]
