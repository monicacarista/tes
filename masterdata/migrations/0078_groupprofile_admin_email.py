# Generated by Django 3.1.7 on 2021-12-08 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0077_auto_20211029_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='admin_email',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
