# Generated by Django 3.2.7 on 2022-01-15 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0019_onlineneftdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeconcession',
            name='fee_submit',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fee.feesubmit'),
        ),
    ]