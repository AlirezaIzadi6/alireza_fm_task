import os
import re
from django import forms

from file_manager.validators.create_folder import validate_folder_name
from file_manager.validators.path import validate_upload_path
from file_manager.utils.path import get_directory_path

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
        path = get_directory_path('uploads', self.username, upload_path)
        validate_upload_path(folder_name, path)
        return cleaned_data