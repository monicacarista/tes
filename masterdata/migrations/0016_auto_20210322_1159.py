# Generated by Django 3.1.7 on 2021-03-22 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0015_masterkapasitasmesin_tebal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='nama',
            field=models.CharField(max_length=70),
        ),
    ]
