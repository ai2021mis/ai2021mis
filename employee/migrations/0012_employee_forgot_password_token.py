# Generated by Django 3.2.6 on 2022-03-05 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0011_alter_employee_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='forgot_password_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
