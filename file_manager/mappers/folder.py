from file_manager.models import Folder
from file_manager.dto.folder import FolderDtoForIndex

def get_folder_dto_for_index(folder: Folder) -> FolderDtoForIndex:
    return FolderDtoForIndex(folder)