# Generated by Django 3.2.6 on 2021-11-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0044_yolo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='yolo',
            name='image_shape',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
