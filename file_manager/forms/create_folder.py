import os
import re
from django import forms

from file_manager.utils.file_validator import validate_upload_path

def validate_folder_name(value):
    invalid_folder_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(invalid_folder_name_regex, value) is None:
        raise forms.ValidationError('Not allowed characters in folder name')
    if len(value) > 255:
        raise forms.ValidationError('Maximum folder name length exceded')

class CreateFolderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('username', None)
        super().__init__(*args, **kwargs)
    
    name = forms.CharField(validators=[validate_folder_name])
    upload_path = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), max_length=4000, required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        folder_name = cleaned_data.get('name')
        upload_path = cleaned_data.get('upload_path')
        validate_upload_path(folder_name, upload_path, self.username)
        return cleaned_data