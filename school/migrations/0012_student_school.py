# Generated by Django 3.2.7 on 2022-01-16 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_alter_student_add_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.school'),
        ),
    ]
