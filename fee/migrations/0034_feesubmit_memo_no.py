# Generated by Django 3.2.7 on 2022-02-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0033_auto_20220125_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='feesubmit',
            name='memo_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
