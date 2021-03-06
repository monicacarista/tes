# Generated by Django 3.1.7 on 2021-06-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0084_detailmaterialconsumption_qty_pakai'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailproductionresults',
            name='fg_mass',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='detailproductionresults',
            name='hold_mass',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='detailproductionresults',
            name='total_output',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailmaterialconsumption',
            name='qty_pakai',
            field=models.FloatField(blank=True, null=True, verbose_name='Pakai (kg)'),
        ),
    ]
