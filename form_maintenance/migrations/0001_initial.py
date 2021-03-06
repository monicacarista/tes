# Generated by Django 3.1.7 on 2021-12-22 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masterdata', '0082_auto_20211217_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterTechnician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('status', models.CharField(choices=[('1', 'Active'), ('0', 'Inactive')], default='1', max_length=1)),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='MasterMachinePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='BreakdownForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_form', models.CharField(max_length=32)),
                ('status', models.CharField(choices=[('1', 'Active'), ('0', 'Closed')], default='1', max_length=1)),
                ('report_time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('breakdown_type', models.CharField(choices=[('1', 'Mechanical'), ('2', 'Electrical')], max_length=1)),
                ('breakdown_note', models.TextField()),
                ('fixing_note', models.TextField()),
                ('broken_part', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='form_maintenance.mastermachinepart')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masterdata.mastermesin')),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='form_maintenance.mastertechnician')),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group')),
            ],
        ),
    ]
