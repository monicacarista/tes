# Generated by Django 3.1.7 on 2021-08-06 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0046_auto_20210726_1425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mastergroup',
            options={'ordering': ['group'], 'verbose_name_plural': 'Master Item Group'},
        ),
        migrations.AlterModelOptions(
            name='mastermesin',
            options={'ordering': ['mesin'], 'verbose_name_plural': 'Master Machine'},
        ),
        migrations.AlterModelOptions(
            name='mastertipe',
            options={'ordering': ['tipe'], 'verbose_name_plural': 'Master Item Type'},
        ),
        migrations.AlterModelOptions(
            name='masteruom',
            options={'ordering': ['uom'], 'verbose_name_plural': 'Master UOM'},
        ),
        migrations.AlterModelOptions(
            name='masterworker',
            options={'ordering': ['nama'], 'verbose_name_plural': 'Master Workers'},
        ),
    ]