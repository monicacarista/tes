# Generated by Django 3.2.11 on 2022-02-03 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0012_settingreject'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SettingReject',
        ),
        migrations.AlterModelOptions(
            name='settingmastergroupqc',
            options={'verbose_name': 'SET 2. QC Parameter', 'verbose_name_plural': 'SET 2. QC Paramater'},
        ),
    ]