from PIL import Image

from file_manager.utils.file_processor import verify_directory_existance

def create_image_thumbnail(name, source_path, destination_path):
    verify_directory_existance(destination_path)
    img = Image.open(source_path+'/'+name)
    img.thumbnail((100, 100))
    img.save(destination_path+'/'+name+'.jpg')

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

def get_image_dimensions(file_path):
    img = Image.open(file_path)
    return img.size