# Generated by Django 3.1.7 on 2021-03-22 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0014_masterkapasitasmesin_warna'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterkapasitasmesin',
            name='tebal',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
