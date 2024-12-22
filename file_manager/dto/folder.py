from file_manager.models import Folder

class FolderDtoForIndex:
    def __init__(self, folder: Folder):
        self.id: int = folder.id
        self.name: str = folder.name
        self.path: str = folder.path
        self.create_date: str = folder.create_date.strftime('%y/%m/%d %H:%M:%S')
        self.update_date: str = folder.update_date.strftime('%y/%m/%d %H:%M:%S')
        self.resource_type: str = 'folder'