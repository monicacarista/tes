# Generated by Django 3.1.7 on 2021-03-15 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0010_reportperhari'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReportPerHari',
        ),
        migrations.CreateModel(
            name='ReportPerWaktu',
            fields=[
            ],
            options={
                'verbose_name': 'Report By Waktu',
                'verbose_name_plural': 'Report By Waktu',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('form_produksi.reportshiftperkk',),
        ),
    ]
