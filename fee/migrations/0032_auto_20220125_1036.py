# Generated by Django 3.2.7 on 2022-01-25 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0031_miscfee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feestruct',
            name='month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fee.month'),
        ),
        migrations.AlterField(
            model_name='feestructbymonth',
            name='month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fee.month'),
        ),
    ]
