# Generated by Django 3.2.7 on 2022-01-15 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0014_feestructbymonth_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeconcession',
            name='reason',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
    ]
