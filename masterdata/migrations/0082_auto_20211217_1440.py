# Generated by Django 3.1.7 on 2021-12-17 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0081_mastermesin_add_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastermesin',
            name='priority',
            field=models.CharField(choices=[('1', 'Main Machine'), ('2', 'Secondary Machine')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='daily_work_hour',
            field=models.FloatField(help_text='Lama jam kerja dari unit dalam sehari'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='shift_hour',
            field=models.DurationField(help_text='Jam mulai kerja shift pertama, mis: 07:00:00'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='weekly_days',
            field=models.CharField(help_text='Isi dengan 1111111 jika grup aktif senin-minggu, 1111100 jika grup aktif senin-jumat, dst (1=Kerja, 0=Libur)', max_length=7),
        ),
        migrations.AlterField(
            model_name='masterbarang',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masterdata.mastergroup', verbose_name='Item Group'),
        ),
        migrations.AlterField(
            model_name='mastergroup',
            name='group',
            field=models.CharField(max_length=40, verbose_name='Item Group'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='dimensi_aux',
            field=models.FloatField(blank=True, null=True, verbose_name='Other Dimension (mm)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='group',
            field=models.ForeignKey(blank=True, limit_choices_to={'tipe__in': [2, 3]}, null=True, on_delete=django.db.models.deletion.PROTECT, to='masterdata.mastergroup', verbose_name='Item Group'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='output_ideal',
            field=models.FloatField(default=0, verbose_name='Output Standar (kg/h or pcs/h)'),
        ),
        migrations.AlterField(
            model_name='masterkapasitasmesin',
            name='tebal',
            field=models.FloatField(blank=True, null=True, verbose_name='Thickness (mm)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='factory_group',
            field=models.ManyToManyField(help_text='Grup Pabrik yang bisa dipakai untuk filter laporan', limit_choices_to={'groupprofile__group_type': '1'}, related_name='other_ug', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='main_group',
            field=models.ForeignKey(blank=True, help_text='Grup Pabrik yang akan menjadi identitas form yang diisi user', limit_choices_to={'groupprofile__group_type': '1'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='main_ug', to='auth.group'),
        ),
    ]
