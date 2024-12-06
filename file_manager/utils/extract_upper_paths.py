from file_manager.models import Folder

def extract_upper_folders(current):
    if current == None or current.parent_folder == None:
        return []
    print(current.parent_folder)
    result = []
    current_parent = current.parent_folder
    while current_parent != None:
        result.append(current_parent)
        current_parent = current_parent.parent_folder
    return result