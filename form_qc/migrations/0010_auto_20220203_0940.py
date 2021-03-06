# Generated by Django 3.2.11 on 2022-02-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0009_parameterformselection_kategori'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masterreject',
            name='aspekCritical',
        ),
        migrations.RemoveField(
            model_name='masterreject',
            name='aspekFungsional',
        ),
        migrations.RemoveField(
            model_name='masterreject',
            name='aspekParameter',
        ),
        migrations.AddField(
            model_name='rejectformselection',
            name='aspekCritical',
            field=models.CharField(choices=[('critical', 'Critical'), ('non_critical', 'Non Critical')], default='pilih salah satu', max_length=50, verbose_name='Aspek Critical'),
        ),
        migrations.AddField(
            model_name='rejectformselection',
            name='aspekFungsional',
            field=models.CharField(choices=[('fungsional', 'Fungsional'), ('estetika', 'Estetika')], default='pilih salah satu', max_length=50, verbose_name='Aspek Fungsional'),
        ),
        migrations.AddField(
            model_name='rejectformselection',
            name='aspekParameter',
            field=models.CharField(choices=[('dimensi', 'Dimensi'), ('atribut', 'Atribut')], default='pilih salah satu', max_length=50, verbose_name='Aspek Parameter'),
        ),
        migrations.RemoveField(
            model_name='rejectformselection',
            name='reject_type',
        ),
        migrations.AddField(
            model_name='rejectformselection',
            name='reject_type',
            field=models.ManyToManyField(related_name='jenis_reject', to='form_qc.MasterReject'),
        ),
    ]
