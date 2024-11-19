# Generated by Django 5.1.3 on 2024-11-17 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0005_alter_uploadmodel_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='upload_path',
            field=models.CharField(max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadmodel',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]