# Generated by Django 3.1.7 on 2021-04-22 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0041_remove_detailmaterialconsumption_reject_pkg'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportshiftperkk',
            name='fg_qty',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
