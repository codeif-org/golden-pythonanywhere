# Generated by Django 3.2.7 on 2022-01-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0021_auto_20220123_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='class_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
