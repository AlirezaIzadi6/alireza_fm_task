from django import forms

from file_manager.utils.path import get_directory_path
from file_manager.validators.create_file import validate_file_name, validate_file_size, validate_file_type
from file_manager.validators.path import validate_upload_path

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