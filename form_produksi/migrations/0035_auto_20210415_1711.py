# Generated by Django 3.1.7 on 2021-04-15 10:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0034_auto_20210415_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailproductionresults',
            name='hold_qc_qty',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]