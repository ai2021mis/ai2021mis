# Generated by Django 3.2.6 on 2021-08-25 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0002_alter_file_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
