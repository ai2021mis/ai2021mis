# Generated by Django 3.2.6 on 2022-03-05 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_employee_forgot_password_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='forgot_password_token',
        ),
    ]