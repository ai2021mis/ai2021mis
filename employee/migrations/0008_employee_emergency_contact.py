# Generated by Django 3.2.6 on 2021-11-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20211126_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='emergency_contact',
            field=models.TextField(blank=True, null=True),
        ),
    ]