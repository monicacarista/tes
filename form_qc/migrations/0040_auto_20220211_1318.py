# Generated by Django 3.2.11 on 2022-02-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0039_auto_20220211_1116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailqcinspection',
            old_name='berat',
            new_name='berat1',
        ),
        migrations.AddField(
            model_name='detailqcinspection',
            name='berat2',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='detailqcinspection',
            name='berat3',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='detailqcinspection',
            name='berat4',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='detailqcinspection',
            name='berat5',
            field=models.FloatField(default=0),
        ),
    ]
