# Generated by Django 3.1.7 on 2021-05-24 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0065_auto_20210524_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportDowntimePerMesin',
            fields=[
            ],
            options={
                'verbose_name': '9. Report Downtime Per Mesin',
                'verbose_name_plural': '9. Report Downtime Per Mesin',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('form_produksi.reportshiftperkk',),
        ),
        migrations.AddField(
            model_name='detaildowntime',
            name='durasi',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
