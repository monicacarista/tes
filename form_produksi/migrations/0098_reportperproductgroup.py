# Generated by Django 3.1.7 on 2021-07-19 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0097_auto_20210715_0810'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportPerProductGroup',
            fields=[
            ],
            options={
                'verbose_name': 'SM6. Report By Product Group',
                'verbose_name_plural': 'SM6. Report By Product Group',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('form_produksi.kk',),
        ),
    ]
