# Generated by Django 3.2.6 on 2021-09-29 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0029_auto_20210928_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='yolo_files',
            name='picture_box',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
