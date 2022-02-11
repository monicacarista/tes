# Generated by Django 3.1.7 on 2021-05-18 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0058_reportshiftperkk_output_std'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kk',
            options={'verbose_name_plural': '1. Daftar KK'},
        ),
        migrations.AlterModelOptions(
            name='reportbykk',
            options={'verbose_name_plural': '6. Report By KK'},
        ),
        migrations.AlterModelOptions(
            name='reportdowntime',
            options={'verbose_name_plural': '5. Downtime'},
        ),
        migrations.AlterModelOptions(
            name='reportmaterialconsumption',
            options={'verbose_name_plural': '4. Material Consumption'},
        ),
        migrations.AlterModelOptions(
            name='reportperwaktu',
            options={'verbose_name': '7. Report By Waktu', 'verbose_name_plural': '7. Report By Waktu'},
        ),
        migrations.AlterModelOptions(
            name='reportproductionresults',
            options={'verbose_name_plural': '3. Production Results'},
        ),
        migrations.AlterModelOptions(
            name='reportshiftperkk',
            options={'ordering': ['-start_time'], 'verbose_name_plural': '2. Form dan Report by Shift'},
        ),
    ]