# Generated by Django 3.1.7 on 2021-09-29 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masterdata', '0061_auto_20210929_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayOffList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('off_day', models.DateField()),
                ('notes', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_type', models.CharField(choices=[('1', 'Unit'), ('0', 'Jabatan')], max_length=1)),
                ('user_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]