from file_manager.models import MediaFile
from file_manager.utils.converters.date_and_time import int_to_time
from file_manager.utils.converters.size import get_readable_size

class FileDtoForIndex:
    def __init__(self, media_file: MediaFile):
        self.id: int = media_file.id
        self.name: str = media_file.name
        self.path: str = media_file.path
        self.type: str = media_file.type
        self.size: int = get_readable_size(media_file.size)
        self.dimensions: str = f'{media_file.width}x{media_file.height}'
        self.duration: str = int_to_time(media_file.length)
        self.create_date: str = media_file.create_date.strftime('%y/%m/%d %H:%M:%S')
        self.update_date: str = media_file.update_date.strftime('%y/%m/%d %H:%M:%S')
        self.resource_type: str = 'file'