import os
from pathlib import Path
import shutil

def save_file(file, path):
    with open(path+'/'+file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def create_directory(path):
    os.mkdir(path)

def verify_directory_existance(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def read_file(path):
    if not os.path.isfile(path):
        return None
    with open(path, 'rb') as f:
        file_content = f.read()
        return file_content

def rename(path: str, old_name: str, new_name: str):
    old_path = os.path.join(path, old_name)
    new_path = os.path.join(path, new_name)
    os.rename(old_path, new_path)

def delete_file(path):
    try:
        os.remove(path)
    except:
        print('An error occurred')

def delete_folder(path):
    try:
        shutil.rmtree(path)
    except:
        print('An error occurred')
