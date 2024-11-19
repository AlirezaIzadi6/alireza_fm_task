import os
from django import forms

def upload_path_is_valid(file, path, username):
    destination_path = f"uploads/{username}{path}"
    destination_file = f"{destination_path}/{file.name}"
    if not os.path.isdir(destination_path):
        raise forms.ValidationError('Requested upload path doesnt exist')
    if os.path.isfile(destination_file):
        raise forms.ValidationError('File already exists.')
