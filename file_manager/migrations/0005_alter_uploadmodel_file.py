# Generated by Django 5.1.3 on 2024-11-16 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0004_uploadmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='file',
            field=models.FileField(max_length=1048576, upload_to='uploads/'),
        ),
    ]