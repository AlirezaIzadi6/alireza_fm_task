import os
import re
from django.forms import ValidationError

def validate_upload_path(name, path):
    created_path = f'{path}/{name}'
    if not os.path.isdir(path):
        raise ValidationError('Requested upload path doesnt exist')
    if os.path.isfile(created_path) or os.path.isdir(created_path):
        raise ValidationError('Duplicate name')

def path_is_valid(value: str):
    if value == '':
        return True
    if len(value) > 4000:
        return False
    invalid_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(value, invalid_name_regex):
        return False
    path_segments = value.split('/')[:]
    for s in path_segments:
        if s == '':
            return False
    return True

def validate_file_name(filename: str):
    invalid_file_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(invalid_file_name_regex, filename) is None:
        raise ValidationError('Not allowed characters in file name')
    if len(filename) > 100:
        raise ValidationError('Maximum file name length exceded')