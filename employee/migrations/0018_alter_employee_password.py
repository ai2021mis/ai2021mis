# Generated by Django 3.2.6 on 2022-03-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0017_alter_employee_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(blank=True, default='Xzb7nbJ8mV', max_length=50),
        ),
    ]
