# Generated by Django 3.1.7 on 2021-04-21 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0029_auto_20210421_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='group',
            field=models.ForeignKey(blank=True, limit_choices_to={'tipe__in': [2, 3]}, null=True, on_delete=django.db.models.deletion.PROTECT, to='masterdata.mastergroup'),
        ),
    ]
