# Generated by Django 3.1.7 on 2021-03-26 07:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0017_auto_20210324_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterbarang',
            name='lebar',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
