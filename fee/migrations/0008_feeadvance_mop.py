# Generated by Django 3.2.7 on 2021-12-23 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0007_auto_20211222_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeadvance',
            name='mop',
            field=models.CharField(default='Cash', max_length=50),
        ),
    ]
