# Generated by Django 3.2.7 on 2022-01-16 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_alter_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='roll_no',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
