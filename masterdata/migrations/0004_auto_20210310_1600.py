# Generated by Django 3.1.7 on 2021-03-10 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0003_auto_20210308_1613'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MasterProfil',
            new_name='MasterProperty',
        ),
        migrations.AlterModelOptions(
            name='masterproperty',
            options={'verbose_name_plural': 'Master Property'},
        ),
        migrations.RenameField(
            model_name='masterbarang',
            old_name='profil',
            new_name='prop1',
        ),
        migrations.RenameField(
            model_name='masterbarang',
            old_name='lebar',
            new_name='tebal1',
        ),
        migrations.RenameField(
            model_name='masterbarang',
            old_name='tebal',
            new_name='tebal2',
        ),
        migrations.RenameField(
            model_name='masterproperty',
            old_name='profil',
            new_name='prop',
        ),
        migrations.RenameField(
            model_name='masterproperty',
            old_name='profil_id',
            new_name='prop_id',
        ),
    ]