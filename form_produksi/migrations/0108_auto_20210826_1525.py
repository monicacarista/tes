# Generated by Django 3.1.7 on 2021-08-26 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0052_auto_20210825_1628'),
        ('form_produksi', '0107_detailfinishedgoodkk'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DetailFinishedGoodKK',
            new_name='DetailKKFinishedGood',
        ),
    ]
