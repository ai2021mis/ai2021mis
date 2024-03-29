# Generated by Django 3.2.6 on 2021-08-26 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0003_alert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert_Yolo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_id', models.SlugField(unique=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('output', models.FileField(blank=True, upload_to='')),
                ('remark', models.TextField(default='(none)')),
            ],
            options={
                'db_table': 'Alert_Yolo',
            },
        ),
        migrations.CreateModel(
            name='Yolo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yolo_id', models.SlugField(unique=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('output', models.FileField(upload_to='')),
                ('remark', models.TextField(default='(none)')),
                ('version', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Yolo',
            },
        ),
        migrations.DeleteModel(
            name='Alert',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.AddField(
            model_name='alert_yolo',
            name='yolo_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='yoloid', to='db_api.yolo'),
        ),
    ]
