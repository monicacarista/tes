# Generated by Django 3.1.7 on 2021-11-02 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0077_auto_20211029_1611'),
        ('form_produksi', '0118_kk_item_example'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kk',
            name='item_example',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masterdata.masterbarang'),
        ),
    ]
