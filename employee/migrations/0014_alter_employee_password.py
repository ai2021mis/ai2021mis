# Generated by Django 3.2.6 on 2022-03-04 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0013_alter_employee_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(blank=True, default='keTACoXERz', max_length=50),
        ),
    ]
