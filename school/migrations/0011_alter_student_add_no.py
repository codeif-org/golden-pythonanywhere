# Generated by Django 3.2.7 on 2022-01-16 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_alter_student_roll_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='add_no',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]