# Generated by Django 3.1.7 on 2021-05-25 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0066_auto_20210524_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detaildowntime',
            name='kategori',
            field=models.CharField(choices=[('1', 'Produksi'), ('3', 'Set up'), ('5', 'Cleaning Mesin/ Warna'), ('2', 'Teknik: Mekanik'), ('7', 'Teknik: Elektrik'), ('4', 'Mati Listrik'), ('L', 'Lain-lain'), ('9', 'Istirahat')], max_length=1),
        ),
    ]
