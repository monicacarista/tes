# Generated by Django 3.2.11 on 2022-02-07 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0029_alter_detailqcinspection_rheovis_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailqcinspection',
            name='bonding_strength_coil_atas',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='detailqcinspection',
            name='bonding_strength_coil_bwh',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='detailqcinspection',
            name='fineness_post_adjusting',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='detailqcinspection',
            name='fineness_pre_adjusting',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='detailqcinspection',
            name='reject',
            field=models.ManyToManyField(related_name='reject', to='form_qc.MasterReject'),
        ),
        migrations.AlterField(
            model_name='detailqcinspection',
            name='reject_indecisive',
            field=models.ManyToManyField(related_name='ragu', to='form_qc.RejectFormSelection'),
        ),
        migrations.AlterField(
            model_name='detailqcinspection',
            name='speed_extruder_adhesive',
            field=models.FloatField(default=None, null=True),
        ),
    ]