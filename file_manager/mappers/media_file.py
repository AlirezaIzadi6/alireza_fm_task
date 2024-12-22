from file_manager.models import MediaFile
from file_manager.dto.media_file import FileDtoForIndex

def get_file_dto_for_index(media_file: MediaFile) -> FileDtoForIndex:
    return FileDtoForIndex(media_file)