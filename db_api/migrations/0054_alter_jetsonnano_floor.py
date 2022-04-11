# Generated by Django 3.2.6 on 2022-03-13 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0053_alter_jetsonnano_floor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jetsonnano',
            name='floor',
            field=models.IntegerField(default=0, help_text="Each camera assign for one floor -- '0' means groundfloor -- '-1..' is basement", unique=True),
        ),
    ]