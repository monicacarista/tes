# Generated by Django 3.1.7 on 2021-03-17 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0007_remove_masterstatus_status_id'),
        ('form_produksi', '0014_auto_20210317_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='foreman',
            field=models.ForeignKey(limit_choices_to={'aktif': '1', 'status': '2'}, on_delete=django.db.models.deletion.PROTECT, related_name='foreman', to='masterdata.masterworker'),
        ),
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='team',
            field=models.ManyToManyField(limit_choices_to={'aktif': '1', 'status': '1'}, related_name='team', to='masterdata.MasterWorker'),
        ),
    ]