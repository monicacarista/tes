# Generated by Django 3.1.7 on 2021-07-26 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0041_auto_20210622_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='prop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masterdata.masteritemproperty', verbose_name='Property Lain'),
        ),
    ]