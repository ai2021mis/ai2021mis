# Generated by Django 3.2.6 on 2021-09-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('line_id', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'Manager',
            },
        ),
    ]
