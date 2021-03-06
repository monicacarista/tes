# Generated by Django 3.1.7 on 2021-09-29 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0059_auto_20210915_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='main_unit',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='factory_group',
            field=models.ManyToManyField(related_name='other_ug', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='main_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='main_ug', to='auth.group'),
        ),
    ]
