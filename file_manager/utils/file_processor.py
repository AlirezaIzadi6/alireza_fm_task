import os

def save_file(file, upload_path, username):
    name = file.name
    save_path = f"uploads/{username}/{upload_path}/{name}"
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def create_directory(name, path, username):
    destination_path = f'uploads/{username}/{path}{name}'
    os.mkdir(destination_path)