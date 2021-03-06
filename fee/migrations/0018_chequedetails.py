# Generated by Django 3.2.7 on 2022-01-15 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0017_feeconcession_concession_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChequeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cheque_no', models.CharField(max_length=50)),
                ('issued_by', models.CharField(max_length=100)),
                ('bank', models.CharField(blank=True, max_length=50, null=True)),
                ('branch', models.CharField(blank=True, max_length=50, null=True)),
                ('issue_date', models.DateField()),
                ('fee_submit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fee.feesubmit')),
            ],
        ),
    ]
