# Generated by Django 3.1.7 on 2021-10-14 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0071_auto_20211012_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='daily_working_hour',
            field=models.FloatField(default=24),
            preserve_default=False,
        ),
    ]
