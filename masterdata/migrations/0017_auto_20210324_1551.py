# Generated by Django 3.1.7 on 2021-03-24 08:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0016_auto_20210322_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='tebal1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='tebal2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
