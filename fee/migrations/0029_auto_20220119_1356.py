# Generated by Django 3.2.7 on 2022-01-19 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0017_student_session'),
        ('fee', '0028_deletedchequedetails_deletedonlineneftdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='feestruct',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.session'),
        ),
        migrations.AddField(
            model_name='feestructbymonth',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.session'),
        ),
    ]
