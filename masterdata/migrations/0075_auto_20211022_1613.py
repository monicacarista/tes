# Generated by Django 3.1.7 on 2021-10-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0074_groupprofile_weekly_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='weekly_days',
            field=models.CharField(max_length=7),
        ),
    ]
