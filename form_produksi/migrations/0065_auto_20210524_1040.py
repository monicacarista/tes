# Generated by Django 3.1.7 on 2021-05-24 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0064_reportshiftperkk_trial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detaildowntime',
            name='kategori',
            field=models.CharField(choices=[('1', 'Produksi'), ('3', 'Set up'), ('5', 'Cleaning Mesin/ Warna'), ('2', 'Teknik: Mekanik'), ('7', 'Teknik: Elektrik'), ('4', 'Mati Listrik'), ('6', 'Lain-lain'), ('9', 'Istirahat')], max_length=1),
        ),
    ]
