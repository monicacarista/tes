# Generated by Django 3.1.7 on 2021-10-05 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0068_auto_20211004_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterbarang',
            name='profil',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='masterdata.masteritemproperty'),
            preserve_default=False,
        ),
    ]
