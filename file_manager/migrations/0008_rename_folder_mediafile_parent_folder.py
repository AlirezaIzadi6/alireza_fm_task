# Generated by Django 5.1.3 on 2024-12-02 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0007_alter_mediafile_folder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediafile',
            old_name='folder',
            new_name='parent_folder',
        ),
    ]
