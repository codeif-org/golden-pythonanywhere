# Generated by Django 3.2.7 on 2022-01-18 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0025_alter_chequedetails_fee_submit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineneftdetails',
            name='fee_submit',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fee_online', to='fee.feesubmit'),
        ),
    ]
