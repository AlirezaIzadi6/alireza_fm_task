import subprocess
from PIL import Image

from file_manager.utils.file_processor import verify_directory_existance

def create_image_thumbnail(name, path, username):
    source_path = '/'.join(['uploads', username, path])
    destination_path = '/'.join(['thumbnails', username, path])
    verify_directory_existance(['thumbnails', username, path])
    img = Image.open(source_path+'/'+name)
    img.thumbnail((100, 100))
    img.save(destination_path+'/'+name+'.jpg')

def create_video_thumbnail(name, path, username):
    source_path = '/'.join(['uploads', username, path])
    destination_path = '/'.join(['thumbnails', username, path])
    verify_directory_existance(['thumbnails', username, path])
    subprocess.call(['ffmpeg', '-i', f'{source_path}/{name}', '-ss', '00:00:00.000', '-vframes', '1', '-vf', 'scale=100:100', f'{destination_path}/{name}.jpg'])