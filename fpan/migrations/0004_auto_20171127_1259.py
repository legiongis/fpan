# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-27 12:59
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fpan', '0003_auto_20171127_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managedarea',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]