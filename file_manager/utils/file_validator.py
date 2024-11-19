import os
import re
from django import forms

def validate_upload_path(name, path, username):
    if path == '':
        destination_path = f'uploads/{username}'
    else:
        destination_path = f'uploads/{username}/{path}'
    created_path = f'{destination_path}/{name}'
    if not os.path.isdir(destination_path):
        raise forms.ValidationError('Requested upload path doesnt exist')
    if os.path.isfile(created_path) or os.path.isdir(created_path):
        raise forms.ValidationError('Duplicate name')

def path_is_valid(str):
    if str == '':
        return True
    if len(str) > 4000:
        return False
    invalid_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(str, invalid_name_regex):
        return False
    path_segments = str.split('/')[:]
    for s in path_segments:
        if s == '':
            return False
    return True