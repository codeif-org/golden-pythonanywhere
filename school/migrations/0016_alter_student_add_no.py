# Generated by Django 3.2.7 on 2022-01-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0015_alter_session_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='add_no',
            field=models.CharField(max_length=50),
        ),
    ]