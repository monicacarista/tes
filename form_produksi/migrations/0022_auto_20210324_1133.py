# Generated by Django 3.1.7 on 2021-03-24 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0021_auto_20210324_0846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportshiftperkk',
            options={'ordering': ['-production_date'], 'verbose_name_plural': '1. Form dan Report by Shift'},
        ),
    ]
