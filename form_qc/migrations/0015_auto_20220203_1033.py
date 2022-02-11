# Generated by Django 3.2.11 on 2022-02-03 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0014_auto_20220203_1011'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MasterRejectSet',
        ),
        migrations.AlterModelOptions(
            name='masterreject',
            options={'verbose_name': 'Master Reject'},
        ),
        migrations.AlterModelOptions(
            name='settingmastergroupqc1',
            options={'verbose_name': 'SET 2. QC Reject', 'verbose_name_plural': 'SET 2. QC Reject'},
        ),
        migrations.RemoveField(
            model_name='rejectformselection',
            name='reject_type',
        ),
        migrations.AddField(
            model_name='rejectformselection',
            name='reject_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='form_qc.masterreject', verbose_name='Jenis Reject'),
        ),
    ]