# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-27 13:19
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('region_code', models.CharField(max_length=4)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Scout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('zip_code', models.CharField(max_length=5)),
                ('phone', models.CharField(max_length=12)),
                ('background', models.TextField(verbose_name=b'Please let us know a little about your education and occupation.')),
                ('relevant_experience', models.TextField(verbose_name=b'Please let us know about any relevant experience.')),
                ('interest_reason', models.TextField(verbose_name=b'Why are you interested in becoming a Heritage Monitoring Scout?')),
                ('site_interest_type', models.CharField(choices=[(b'Prehistoric', b'Prehistoric'), (b'Historic', b'Historic'), (b'Cemeteries', b'Cemeteries'), (b'Underwater', b'Underwater'), (b'Other', b'Other')], max_length=30, verbose_name=b'What type of sites are you interested in?')),
                ('ethics_agreement', models.BooleanField()),
                ('region_choices', models.ManyToManyField(to='fpan.Region')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
