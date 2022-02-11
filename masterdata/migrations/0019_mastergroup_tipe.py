# Generated by Django 3.1.7 on 2021-04-01 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0018_masterbarang_lebar'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastergroup',
            name='tipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='masterdata.mastertipe'),
            preserve_default=False,
        ),
    ]
