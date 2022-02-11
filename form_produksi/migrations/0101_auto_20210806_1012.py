# Generated by Django 3.1.7 on 2021-08-06 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0046_auto_20210726_1425'),
        ('form_produksi', '0100_auto_20210726_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='foreman',
            field=models.ForeignKey(blank=True, limit_choices_to={'aktif': '1'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='foreman', to='masterdata.masterworker'),
        ),
    ]