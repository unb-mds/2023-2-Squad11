# Generated by Django 4.2.5 on 2023-11-06 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_department_code_alter_discipline_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='code',
            field=models.CharField(max_length=20),
        ),
    ]