# Generated by Django 3.1.7 on 2021-05-21 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_produksi', '0061_auto_20210518_0903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportdowntime',
            options={'verbose_name_plural': '5. Report Downtime'},
        ),
        migrations.AlterModelOptions(
            name='reportmaterialconsumption',
            options={'verbose_name_plural': '4. Report Material Consumption'},
        ),
        migrations.AlterModelOptions(
            name='reportproductionresults',
            options={'verbose_name_plural': '3. Report Production Results'},
        ),
        migrations.AlterModelOptions(
            name='reportrejectpacakging',
            options={'verbose_name_plural': '8. Report Reject Packaging'},
        ),
        migrations.AlterField(
            model_name='reportshiftperkk',
            name='output_std',
            field=models.FloatField(blank=True, null=True, verbose_name='Out Std'),
        ),
    ]
