# Generated by Django 3.2.6 on 2021-09-25 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0023_rename_yoloid_yolo_files_yolo_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yolo_files',
            old_name='yolo_id',
            new_name='yoloid',
        ),
        migrations.AlterField(
            model_name='alert_data',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
