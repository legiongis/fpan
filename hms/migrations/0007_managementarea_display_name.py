# Generated by Django 2.2.13 on 2021-06-15 11:31

from django.db import migrations, models

from hms.models import ManagementArea

def update_existing_management_areas(apps, schema_editor):
    for ma in ManagementArea.objects.all():
        ma.save(update_fields=['display_name'])

def reversible_placeholder(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0006_userxresourceinstanceaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='managementarea',
            name='display_name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.RunPython(update_existing_management_areas, reversible_placeholder)
    ]