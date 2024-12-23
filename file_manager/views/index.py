from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Constants:
from file_manager.constants.directory import UPLOADS_FOLDER
# Data access helpers:
from file_manager.data_access_helpers.file_or_folder import get_file_or_folder
# Mappers:
from file_manager.mappers.folder import get_folder_dto_for_index
from file_manager.mappers.media_file import get_file_dto_for_index
# Models:
from file_manager.models import Folder, MediaFile
#Utils:
from file_manager.utils.file_processor import read_file
from file_manager.utils.file_validator import path_is_valid
from file_manager.utils.path import extract_upper_folders, split_path_and_name, get_file_path

@login_required
def index(request, path=''):
    if not path_is_valid(path):
        return redirect('index')
    # Get path and name of the requested resource:
    parent_path, name = split_path_and_name(path)
    file_or_folder = get_file_or_folder(parent_path, name, request.user)
    if file_or_folder is None:
        return redirect('index')
    if file_or_folder.resource_type == 'folder':
        current_folder = file_or_folder.resource
        folders = Folder.objects.filter(path=path, creator=request.user)
        files = MediaFile.objects.filter(path=path, creator=request.user)
        upper_folders = [get_folder_dto_for_index(f) for f in extract_upper_folders(current_folder)]
        data = []
        for f in folders:
            new_item = get_folder_dto_for_index(f)
            data.append(new_item)
        for f in files:
            new_item = get_file_dto_for_index(f)
            data.append(new_item)
        context = {'current_path': path, 'current_folder': name, 'data': data, 'upper_folders': upper_folders}
        return render(request, 'index.html', context)
    elif file_or_folder.resource_type == 'file':
        file_path = get_file_path(UPLOADS_FOLDER, request.user.username, parent_path, name)
        file_content = read_file(file_path)
        response = HttpResponse(file_content, content_type=file_or_folder.resource.type)
        return response
