import re
import subprocess
from PIL import Image

from file_manager.utils.file_processor import verify_directory_existance

def create_image_thumbnail(name, source_path, destination_path):
    verify_directory_existance(destination_path)
    img = Image.open(source_path+'/'+name)
    img.thumbnail((100, 100))
    img.save(destination_path+'/'+name+'.jpg')

def create_video_thumbnail(name, source_path, destination_path):
    verify_directory_existance(destination_path)
    subprocess.call(['ffmpeg', '-i', f'{source_path}/{name}', '-ss', '00:00:00.000', '-vframes', '1', '-vf', 'scale=100:100', f'{destination_path}/{name}.jpg'])

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

def is_valid_video(file_path):
    result = subprocess.run(['ffmpeg', '-i', file_path], capture_output=True, text=True)
    output = result.stderr
    pattern = 'Duration: \\d'
    if re.search(pattern, output) is None:
        return False
    return True