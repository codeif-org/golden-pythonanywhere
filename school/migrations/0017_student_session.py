# Generated by Django 3.2.7 on 2022-01-19 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0016_alter_student_add_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.session'),
        ),
    ]
