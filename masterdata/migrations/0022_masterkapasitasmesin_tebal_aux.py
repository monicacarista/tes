# Generated by Django 3.1.7 on 2021-04-08 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0021_auto_20210405_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterkapasitasmesin',
            name='tebal_aux',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
