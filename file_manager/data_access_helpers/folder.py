from file_manager.models import Folder

def get_folder_by_path(path, user):
    if path == '':
        return None
    path_parts = path.split('/')
    if len(path_parts) == 1:
        try:
            return Folder.objects.get(name=path, parent_folder=None, creator=user)
        except:
            return None
    name = path_parts[-1]
    parent_path = '/'.join(path_parts[:-1])
    try:
        return Folder.objects.get(name=name, path=parent_path, creator=user)
    except:
        return None