import json

def format_folder_info(folder):
    result = {}
    result['Folder name'] = folder.name
    result['Created at'] = folder.create_date.strftime('%d/%m/%y %H:%M:%S')
    result['Updated at'] = folder.update_date.strftime('%d/%m/%y %H:%M:%S')
    result['path'] = '/'+folder.path
    return json.dumps(result, default=str)

def format_file_info(file):
    result = {}
    result['File name'] = file.name
    result['File type'] = file.type
    result['Size'] = file.size
    result['Uploaded at'] = file.create_date.strftime('%d/%m/%y %H:%M:%S')
    result['Updated at'] = file.update_date.strftime('%d/%m/%y %H:%M:%S')
    result['path'] = '/'+file.path
    return json.dumps(result, default=str)