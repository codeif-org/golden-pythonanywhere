# Generated by Django 3.2.7 on 2022-01-18 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0023_feesubmit_submit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesubmit',
            name='submit_date',
            field=models.DateField(),
        ),
    ]