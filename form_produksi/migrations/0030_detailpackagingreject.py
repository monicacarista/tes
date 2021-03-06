# Generated by Django 3.1.7 on 2021-04-12 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0024_masterbarang_aktif'),
        ('form_produksi', '0029_auto_20210408_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailPackagingReject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reject', models.IntegerField()),
                ('laporan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_produksi.reportshiftperkk')),
                ('packaging', models.ForeignKey(limit_choices_to={'aktif': 1, 'tipe__in': [4]}, on_delete=django.db.models.deletion.PROTECT, to='masterdata.masterbarang')),
            ],
        ),
    ]
