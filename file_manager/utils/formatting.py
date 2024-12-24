import json

from file_manager.models import Folder, MediaFile
from file_manager.utils.converters.date_and_time import int_to_time
from file_manager.utils.converters.size import get_readable_size

def format_folder_info(folder: Folder) -> dict:
    result = {}
    result['Folder name'] = folder.name
    result['Created at'] = folder.create_date.strftime('%d/%m/%y %H:%M:%S')
    result['Updated at'] = folder.update_date.strftime('%d/%m/%y %H:%M:%S')
    result['path'] = '/'+folder.path
    return json.dumps(result, default=str)

def format_file_info(file: MediaFile) -> dict:
    result = {}
    result['File name'] = file.name
    result['File type'] = file.type
    result['Size'] = get_readable_size(file.size)
    result['Dimensions'] = f'{file.width}x{file.height}'
    if 'video' in file.type:
        result['Duration'] = int_to_time(file.length)
    result['Uploaded at'] = file.create_date.strftime('%d/%m/%y %H:%M:%S')
    result['Updated at'] = file.update_date.strftime('%d/%m/%y %H:%M:%S')
    result['path'] = '/'+file.path
    return json.dumps(result, default=str)