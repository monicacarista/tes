# Generated by Django 3.1.7 on 2021-04-16 02:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0025_auto_20210413_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='gsm',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='GSM (mm)'),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='lebar',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Lebar Efektif (mm)'),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='lebar_ext',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Lebar Bentang (mm)'),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='panjang',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Panjang (mm)'),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='tebal1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tebal Utama (mm)'),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='tebal2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tebal Lain (mm)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='dimensi_aux',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Dimensi lain (mm)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='dl_standar',
            field=models.PositiveIntegerField(verbose_name='DL Standar (Person)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='output_ideal',
            field=models.FloatField(default=0, verbose_name='Output Standar (kg/h)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='tebal',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Tebal (mm)'),
        ),
    ]