# Generated by Django 3.1.7 on 2021-04-22 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0039_auto_20210421_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailmaterialconsumption',
            name='reject_pkg',
            field=models.FloatField(default=0, verbose_name='Reject Pkg (pcs)'),
        ),
    ]
