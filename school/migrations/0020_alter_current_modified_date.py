# Generated by Django 3.2.7 on 2022-01-22 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0019_alter_student_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='current',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
