# Generated by Django 3.1.7 on 2021-03-19 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0013_remove_masterkapasitasmesin_warna'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterkapasitasmesin',
            name='warna',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='masterdata.masterwarna'),
            preserve_default=False,
        ),
    ]
