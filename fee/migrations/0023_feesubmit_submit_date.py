# Generated by Django 3.2.7 on 2022-01-18 05:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0022_feesubmit_txn_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='feesubmit',
            name='submit_date',
            field=models.DateField(default=datetime.date(2022, 1, 18)),
        ),
    ]