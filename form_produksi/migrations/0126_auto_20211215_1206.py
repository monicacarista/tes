# Generated by Django 3.1.7 on 2021-12-15 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0125_auto_20211208_1422'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportbykk',
            options={'verbose_name_plural': 'SMW1. Report By WO'},
        ),
        migrations.AlterModelOptions(
            name='reportpermesin',
            options={'verbose_name': 'SMT3. Report Machine vs Time', 'verbose_name_plural': 'SMT3. Report Machine vs Time'},
        ),
        migrations.AlterModelOptions(
            name='reportpermesindetailed',
            options={'verbose_name': 'SMW2. Report By Machine', 'verbose_name_plural': 'SMW2. Report By Machine'},
        ),
        migrations.AlterModelOptions(
            name='reportperproductgroup',
            options={'verbose_name': 'SMW3. Report By Product Group', 'verbose_name_plural': 'SMW3. Report By Product Group'},
        ),
        migrations.AlterModelOptions(
            name='reportperunit',
            options={'verbose_name': 'SMT1. Report By Unit', 'verbose_name_plural': 'SMT1. Report By Unit'},
        ),
        migrations.AlterModelOptions(
            name='reportperwaktu',
            options={'verbose_name': 'SMT2. Report By Time Period', 'verbose_name_plural': 'SMT2. Report By Time Period'},
        ),
    ]
