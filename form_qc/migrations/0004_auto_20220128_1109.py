# Generated by Django 3.2.11 on 2022-01-28 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0003_pengecekanproxy_settingmastergroupqc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pengecekanproxy',
            options={'verbose_name_plural': 'QC'},
        ),
        migrations.AddField(
            model_name='detailqcinspection',
            name='berat',
            field=models.FloatField(default=None),
        ),
    ]
