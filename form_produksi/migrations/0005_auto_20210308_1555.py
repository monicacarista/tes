# Generated by Django 3.1.7 on 2021-03-08 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('form_produksi', '0004_auto_20210308_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='user_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='auth.group'),
        ),
    ]