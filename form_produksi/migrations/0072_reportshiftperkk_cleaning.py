# Generated by Django 3.1.7 on 2021-06-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0071_reportrawmaterialperkk'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportshiftperkk',
            name='cleaning',
            field=models.BooleanField(default=False),
        ),
    ]
