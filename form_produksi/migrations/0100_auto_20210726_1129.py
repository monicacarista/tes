# Generated by Django 3.1.7 on 2021-07-26 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0099_auto_20210723_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportbykk',
            options={'verbose_name_plural': 'SM3. Report By WO'},
        ),
        migrations.AlterModelOptions(
            name='reportpermesin',
            options={'verbose_name': 'SM4. Report Machine vs Time', 'verbose_name_plural': 'SM4. Report Machine vs Time'},
        ),
        migrations.AlterModelOptions(
            name='reportpermesindetailed',
            options={'verbose_name': 'SM5. Report By Machine', 'verbose_name_plural': 'SM5. Report By Machine'},
        ),
        migrations.AlterModelOptions(
            name='reportperwaktu',
            options={'verbose_name': 'SM2. Report By Time Period', 'verbose_name_plural': 'SM2. Report By Time Period'},
        ),
    ]
