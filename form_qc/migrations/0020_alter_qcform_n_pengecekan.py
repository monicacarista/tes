# Generated by Django 3.2.11 on 2022-02-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_qc', '0019_alter_qcform_n_pengecekan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qcform',
            name='n_pengecekan',
            field=models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14')], default='pilih salah satu'),
        ),
    ]
