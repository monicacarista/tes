# Generated by Django 3.1.7 on 2021-04-08 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0023_auto_20210408_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterbarang',
            name='aktif',
            field=models.CharField(choices=[('1', 'Aktif'), ('0', 'Inaktif')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]