# Generated by Django 3.1.7 on 2021-03-08 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0007_auto_20210308_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailmaterialconsumption',
            name='batch_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='detailproductionresults',
            name='batch_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
