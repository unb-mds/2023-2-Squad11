# Generated by Django 4.2.5 on 2023-11-27 15:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_class_workload_class_special_dates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='special_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), size=3), default=list, size=None),
        ),
    ]
