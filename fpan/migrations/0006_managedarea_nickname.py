# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-10 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpan', '0005_auto_20171201_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='managedarea',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]