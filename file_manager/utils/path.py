from file_manager.models import Folder

def extract_upper_folders(current):
    if current == None or current.parent_folder == None:
        return []
    result = []
    current_parent = current.parent_folder
    while current_parent != None:
        result.append(current_parent)
        current_parent = current_parent.parent_folder
    result.reverse()
    return result

def get_directory_path(mode, username, path):
    if path == '':
        return '/'.join([mode, username])
    else:
        return '/'.join([mode, username, path])

def get_file_path(mode, username, path, name):
    if path == '':
        return '/'.join([mode, username, name])
    else:
        return '/'.join([mode, username, path, name])

def split_path_and_name(complete_path: str):
    if complete_path == '':
        name = 'index'
        path = ''
    else:
        path_splitted = complete_path.split('/')
        if len(path_splitted) == 1:
            name = complete_path
            path = ''
        else:
            name = path_splitted[-1]
            path = '/'.join(path_splitted[:-1])
    return path, name