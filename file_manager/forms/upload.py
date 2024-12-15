import os
import re
import uuid
from django import forms

from file_manager.models import UploadModel
from file_manager.utils.file_processor import save_file, verify_directory_existance
from file_manager.utils.file_validator import validate_upload_path
from file_manager.utils.image_processor import is_valid_image, is_valid_video
from file_manager.utils.path import get_directory_path

def validate_file_size(value):
    size_limit = 10*1024*1024
    if value.size > size_limit:
        raise forms.ValidationError('Max allowed file size: 10 MB')

def validate_file_name(value):
    filename = value.name
    invalid_file_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(invalid_file_name_regex, filename) is None:
        raise forms.ValidationError('Not allowed characters in file name')
    if len(filename) > 255:
        raise forms.ValidationError('Maximum file name length exceded')

def validate_file_type(value):
    type = value.content_type.split('/')[0]
    if 'video' not in type and 'image' not in type:
        raise forms.ValidationError('File must be an image or a video')
    temp_folder = str(uuid.uuid4())
    temp_path = f'temp/{temp_folder}'
    verify_directory_existance(temp_path)
    save_file(value, temp_path)
    file_path = temp_path+'/'+value.name
    if type == 'image' and not is_valid_image(file_path):
        raise forms.ValidationError('Image file is invalid')
    if type == 'video' and not is_valid_video(file_path):
        raise forms.ValidationError('Video file is invalid')

class UploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)
    
    file = forms.FileField(validators=[validate_file_size, validate_file_name, validate_file_type])
    upload_path = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), max_length=4000, required=False)

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        upload_path = cleaned_data.get('upload_path')
        if file is not None:
            path = get_directory_path('uploads', self.username, upload_path)
            validate_upload_path(file.name, path)
        return cleaned_data