# Generated by Django 3.2.11 on 2022-02-10 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0035_alter_qcform_inspection_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='qcform',
            name='inspection_time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, verbose_name='Jam Pengecekan'),
        ),
    ]
