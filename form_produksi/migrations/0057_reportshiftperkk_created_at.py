# Generated by Django 3.1.7 on 2021-05-11 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0056_auto_20210503_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportshiftperkk',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]