# Generated by Django 3.2.6 on 2021-10-01 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0030_yolo_files_picture_box'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture_Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, default='', upload_to='Uploaded Files/')),
            ],
        ),
    ]
