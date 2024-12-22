from file_manager.models import MediaFile

class FileDtoForIndex:
    def __init__(self, media_file: MediaFile):
        self.id: int = media_file.id
        self.name: str = media_file.name
        self.path: str = media_file.path
        self.type: str = media_file.type
        self.size: int = media_file.size
        self.create_date: str = media_file.create_date.strftime('%y/%m/%d %H:%M:%S')
        self.update_date: str = media_file.update_date.strftime('%y/%m/%d %H:%M:%S')
        self.resource_type: str = 'file'