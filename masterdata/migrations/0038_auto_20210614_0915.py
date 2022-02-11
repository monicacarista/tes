# Generated by Django 3.1.7 on 2021-06-14 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0037_remove_masterbarang_user_group_aux'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='dimensi_aux',
            field=models.FloatField(blank=True, null=True, verbose_name='Dimensi lain (mm)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='tebal',
            field=models.FloatField(blank=True, null=True, verbose_name='Tebal (mm)'),
        ),
    ]