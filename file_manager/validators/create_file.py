import re
import uuid
from shutil import rmtree

from django.forms import ValidationError

from file_manager.utils.file_processor import save_file, verify_directory_existance
from file_manager.utils.media_tools.image_processor import is_valid_image
from file_manager.utils.media_tools.video_processor import is_valid_video

def validate_file_size(value):
    size_limit = 10*1024*1024
    if value.size > size_limit:
        raise ValidationError('Max allowed file size: 10 MB')

def validate_file_name(value):
    filename = value.name
    invalid_file_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(invalid_file_name_regex, filename) is None:
        raise ValidationError('Not allowed characters in file name')
    if len(filename) > 255:
        raise ValidationError('Maximum file name length exceded')

def validate_file_type(value):
    type = value.content_type.split('/')[0]
    if 'video' not in type and 'image' not in type:
        raise ValidationError('File must be an image or a video')
    temp_folder = str(uuid.uuid4())
    temp_path = f'temp/{temp_folder}'
    verify_directory_existance(temp_path)
    save_file(value, temp_path)
    try:
        file_path = temp_path+'/'+value.name
        if type == 'image' and not is_valid_image(file_path):
            raise ValidationError('Image file is invalid')
        if type == 'video' and not is_valid_video(file_path):
            raise ValidationError('Video file is invalid')
    finally:
        rmtree(temp_path)
