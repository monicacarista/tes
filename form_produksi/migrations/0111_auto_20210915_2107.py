# Generated by Django 3.1.7 on 2021-09-15 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0110_prefilledform'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PrefilledForm',
        ),
        migrations.DeleteModel(
            name='ReportDowntime',
        ),
        migrations.DeleteModel(
            name='ReportDowntimePerMesin',
        ),
        migrations.DeleteModel(
            name='ReportMaterialConsumption',
        ),
        migrations.DeleteModel(
            name='ReportPerMesin',
        ),
        migrations.DeleteModel(
            name='ReportPerUnit',
        ),
        migrations.DeleteModel(
            name='ReportPerWaktu',
        ),
        migrations.DeleteModel(
            name='ReportProductionResults',
        ),
        migrations.DeleteModel(
            name='ReportRejectPacakging',
        ),
    ]