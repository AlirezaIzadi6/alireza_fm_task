import re

from django.forms.forms import ValidationError

def validate_folder_name(value):
    invalid_folder_name_regex = r"^[^\0\/\:\*\?\"\<\>\|]+$"
    if re.match(invalid_folder_name_regex, value) is None:
        raise ValidationError('Not allowed characters in folder name')
    if len(value) > 255:
        raise ValidationError('Maximum folder name length exceded')
