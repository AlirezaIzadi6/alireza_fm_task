from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from file_manager.data_access.folder import get_folder_by_path
from file_manager.data_access.file_or_folder import get_file_or_folder
from file_manager.forms.upload import UploadForm
from file_manager.forms.create_folder import CreateFolderForm
from file_manager.utils.file_validator import path_is_valid
from file_manager.utils.file_processor import save_file, create_directory, verify_user_directory_existance, read_file
from file_manager.utils.path import extract_upper_folders
from file_manager.models import Folder, MediaFile
from file_manager.mappers.path import Resource

@login_required
def index(request, path=''):
    if not path_is_valid(path):
        return redirect('index')
    resource = Resource(path)
    file_or_folder = get_file_or_folder(resource)
    if path == '' or file_or_folder.resource_type == 'folder':
        if path == '':
            current_folder = None
        else:
            current_folder = file_or_folder.resource
        folders = Folder.objects.filter(path=path, creator=request.user)
        files = MediaFile.objects.filter(path=path, creator=request.user)
        upper_folders = extract_upper_folders(current_folder)
        data = list(folders) + list(files)
        context = {'current_path': path, 'current_folder': resource.name, 'parent_folder': resource.path, 'data': data, 'upper_folders': upper_folders}
        return render(request, 'index.html', context)
    elif file_or_folder.resource_type == 'file':
        file_content = read_file(path, request.user.username)
        response = HttpResponse(file_content, content_type=file_or_folder.resource.type)
        response['content-disposition'] = f'attachment; filename="{resource.name}"'
        return response
    else:
        return redirect('index')

@login_required
def upload(request):
    if request.method == 'POST':
        verify_user_directory_existance(request.user.username)
        form = UploadForm(request.POST, request.FILES, username=request.user.username)
        if form.is_valid():
            file = request.FILES['file']
            upload_path = request.POST.get('upload_path')
            parent_folder = get_folder_by_path(upload_path, request.user)
            username = request.user.username
            file_type = file.content_type.split('/')[0]
            save_file(file, upload_path, username)
            MediaFile.objects.create(
                name=file.name,
                path=upload_path,
                type=file_type,
                size=file.size,
                parent_folder=parent_folder,
                creator=request.user,
            )
            if upload_path == '':
                return redirect('index')
            return redirect('index', path=upload_path)
    else:
        upload_path = request.GET.get('upload_path', '')
        form = UploadForm(initial={'upload_path': upload_path})
    return render(request, 'upload.html', {'form': form})


@login_required
def create_folder(request):
    if request.method == 'POST':
        verify_user_directory_existance(request.user.username)
        form = CreateFolderForm(request.POST, username=request.user.username)
        if form.is_valid():
            folder_name = request.POST.get('name')
            upload_path = request.POST.get('upload_path')
            parent_folder = get_folder_by_path(upload_path, request.user)
            username = request.user.username
            create_directory(folder_name, upload_path, username)
            Folder.objects.create(
                name=folder_name,
                path=upload_path,
                parent_folder=parent_folder,
                creator=request.user,
            )
            if upload_path == '':
                return redirect('index')
            return redirect('index', path=upload_path)
    else:
        upload_path = request.GET.get('upload_path', '')
        form = CreateFolderForm(initial={'upload_path': upload_path})
    return render(request, 'create_folder.html', {'form': form})