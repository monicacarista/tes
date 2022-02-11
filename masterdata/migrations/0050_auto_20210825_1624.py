# Generated by Django 3.1.7 on 2021-08-25 16:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0049_masterbarang_berat_standar_fg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='berat_standar_fg',
            field=models.FloatField(default=0, help_text='Jika RM, isi 0', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Berat Standar (FG)'),
            preserve_default=False,
        ),
    ]