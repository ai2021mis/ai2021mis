# Generated by Django 3.2.6 on 2022-03-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0050_jetsonnano'),
    ]

    operations = [
        migrations.AddField(
            model_name='jetsonnano',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jetsonnano',
            name='floor',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
