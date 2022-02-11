# Generated by Django 3.1.7 on 2021-04-06 06:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0021_auto_20210405_1635'),
        ('form_produksi', '0026_auto_20210401_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailproductionresults',
            name='hold_qc_qty',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='foreman',
            field=models.ForeignKey(blank=True, limit_choices_to={'aktif': '1', 'status': 2}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='foreman', to='masterdata.masterworker'),
        ),
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='team',
            field=models.ManyToManyField(blank=True, limit_choices_to={'aktif': '1', 'status': 1}, related_name='team', to='masterdata.MasterWorker'),
        ),
    ]