import os

def save_file(file, upload_path, username):
    name = file.name
    save_path = f"uploads/{username}/{upload_path}/{name}"
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def create_directory(name, path, username):
    destination_path = f'uploads/{username}/{path}/{name}'
    os.mkdir(destination_path)

def verify_user_directory_existance(username):
    if not os.path.isdir(f'uploads/{username}'):
        os.mkdir(f'uploads/{username}')

def read_file(path, username):
    path_parts = ['uploads', username, path]
    complete_path = '/'.join(path_parts)
    if not os.path.isfile(complete_path):
        return None
    with open(complete_path, 'rb') as f:
        file_content = f.read()
        return file_content