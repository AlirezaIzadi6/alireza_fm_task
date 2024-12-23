from accounts.models import CustomUser
from file_manager.models import Folder, MediaFile

class FileOrFolder:
    def __init__(self, resource, resource_type):
        self.resource = resource
        self.resource_type = resource_type

def get_file_or_folder(path: str, name: str, creator: CustomUser):
    if path == '' and name == 'index':
        return FileOrFolder(None, 'folder')
    try:
        folder = Folder.objects.get(path=path, name=name, creator=creator)
        return FileOrFolder(folder, 'folder')
    except Folder.DoesNotExist:
        try:
            file = MediaFile.objects.get(path=path, name=name, creator=creator)
            return FileOrFolder(file, 'file')
        except MediaFile.DoesNotExist:
            return None