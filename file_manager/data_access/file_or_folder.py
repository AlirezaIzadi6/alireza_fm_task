from file_manager.models import Folder, MediaFile

class FileOrFolder:
    def __init__(self, resource, resource_type):
        self.resource = resource
        self.resource_type = resource_type

def get_file_or_folder(resource):
    try:
        folder = Folder.objects.get(path=resource.path, name=resource.name)
        return FileOrFolder(folder, 'folder')
    except Folder.DoesNotExist:
        try:
            file = MediaFile.objects.get(path=resource.path, name=resource.name)
            return FileOrFolder(file, 'file')
        except MediaFile.DoesNotExist:
            return None