# Generated by Django 3.1.7 on 2021-12-17 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0126_auto_20211215_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionform',
            name='fg_split',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='FG Split By Machine (kg)'),
        ),
    ]
