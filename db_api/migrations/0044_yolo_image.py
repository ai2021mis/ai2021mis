# Generated by Django 3.2.6 on 2021-11-10 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0043_alter_yolo_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='yolo',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
