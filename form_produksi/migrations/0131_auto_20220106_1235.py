# Generated by Django 3.1.7 on 2022-01-06 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0130_auto_20220106_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportperwaktu',
            options={'verbose_name': 'SMT2. Report By Form Date', 'verbose_name_plural': 'SMT2. Report By Form Date'},
        ),
        migrations.AlterModelOptions(
            name='reportperwaktuvskk',
            options={'verbose_name': 'SMW2. Report By WO Date', 'verbose_name_plural': 'SMW2. Report By WO Date'},
        ),
    ]
