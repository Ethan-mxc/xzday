# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-17 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='myintr',
            field=models.CharField(max_length=254),
        ),
    ]
