# Generated by Django 3.1.7 on 2021-04-13 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0031_auto_20210413_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='dl_avail',
            field=models.PositiveIntegerField(verbose_name='Jml Man Pwr'),
        ),
    ]
