# Generated by Django 3.1.7 on 2021-10-01 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0115_auto_20210930_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportDowntimePerWaktu',
            fields=[
            ],
            options={
                'verbose_name': 'DT3. Report Downtime Per Waktu',
                'verbose_name_plural': 'DT3. Report Downtime Per Waktu',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('form_produksi.productionform',),
        ),
    ]