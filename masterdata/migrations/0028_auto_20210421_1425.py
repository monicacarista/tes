# Generated by Django 3.1.7 on 2021-04-21 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0027_auto_20210416_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='group',
            field=models.ForeignKey(limit_choices_to={'id__in': [2, 3]}, on_delete=django.db.models.deletion.PROTECT, to='masterdata.mastergroup'),
        ),
    ]
