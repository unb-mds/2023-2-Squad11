# Generated by Django 4.2.5 on 2023-11-06 00:27

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='name',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='_class',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='classroom',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='days',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='teachers',
        ),
        migrations.RemoveField(
            model_name='discipline',
            name='workload',
        ),
        migrations.AddField(
            model_name='department',
            name='period',
            field=models.CharField(default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='department',
            name='year',
            field=models.CharField(default='0000', max_length=4),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workload', models.IntegerField()),
                ('teachers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('classroom', models.CharField(max_length=50)),
                ('schedule', models.CharField(max_length=50)),
                ('days', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('_class', models.IntegerField()),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='api.discipline')),
            ],
        ),
    ]