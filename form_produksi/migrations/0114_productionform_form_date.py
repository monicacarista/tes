# Generated by Django 3.1.7 on 2021-09-30 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0113_auto_20210929_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionform',
            name='form_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
