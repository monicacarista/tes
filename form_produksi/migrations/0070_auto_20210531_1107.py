# Generated by Django 3.1.7 on 2021-05-31 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0069_auto_20210525_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailpackagingusage',
            name='reject',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='detailpackagingusage',
            name='terpakai',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='dl_avail',
            field=models.FloatField(verbose_name='Jml Man Pwr'),
        ),
    ]