# Generated by Django 3.2.6 on 2021-09-28 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0028_yolo_trial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yolo_files',
            name='file',
        ),
        migrations.AddField(
            model_name='yolo_files',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='Uploaded Files/'),
        ),
    ]
