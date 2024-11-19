import os
import re
from django import forms

from file_manager.models import UploadModel
from file_manager.utils.file_validator import upload_path_is_valid

def validate_file_size(value):
    size_limit = 10*1024*1024
    if value.size > size_limit:
        raise forms.ValidationError('Max allowed file size: 10 MB')

def validate_file_name(value):
    filename = value.name
    valid_file_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(valid_file_name_regex, filename) is None:
        raise forms.ValidationError('Not allowed characters in file name')
    if len(filename) > 255:
        raise forms.ValidationError('Maximum file name length exceded')

def validate_file_type(value):
    type = value.content_type
    if 'video' not in type and 'image' not in type:
        raise forms.ValidationError('File must be an image or a video')

class UploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)
    
    file = forms.FileField(validators=[validate_file_size, validate_file_name, validate_file_type])
    upload_path = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), max_length=4000)

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        upload_path = cleaned_data.get('upload_path')
        if file is not None:
            upload_path_is_valid(file, upload_path, self.username)
        return cleaned_data