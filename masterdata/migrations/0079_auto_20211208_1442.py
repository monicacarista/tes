# Generated by Django 3.1.7 on 2021-12-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0078_groupprofile_admin_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='admin_email',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
