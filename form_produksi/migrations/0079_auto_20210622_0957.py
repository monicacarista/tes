# Generated by Django 3.1.7 on 2021-06-22 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0078_auto_20210618_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kk',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='kk',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 22, 9, 57, 25, 759685)),
        ),
    ]
