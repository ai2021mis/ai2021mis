# Generated by Django 3.2.6 on 2021-09-25 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0024_auto_20210925_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yolo_files',
            old_name='yoloid',
            new_name='yolo_id',
        ),
        migrations.RemoveField(
            model_name='yolo_files',
            name='image',
        ),
        migrations.AddField(
            model_name='yolo_files',
            name='file',
            field=models.FileField(blank=True, upload_to='Uploaded Files/'),
        ),
        migrations.AlterField(
            model_name='alert_data',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
