# Generated by Django 3.1.7 on 2021-06-15 14:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0038_auto_20210614_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='tebal1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tebal Utama (mm) / Diameter (inch)'),
        ),
    ]
