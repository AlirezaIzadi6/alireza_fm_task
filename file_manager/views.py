from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from file_manager.forms.upload import UploadForm
from file_manager.forms.create_folder import CreateFolderForm
from file_manager.utils.file_validator import path_is_valid
from file_manager.utils.file_processor import save_file, create_directory, verify_user_directory_existance
from file_manager.models import Folder, MediaFile

@login_required
def index(request, path=''):
    if not path_is_valid(path):
        return redirect('index')
    resource_name = path.split('/')[-1]
    if resource_name == '':
        resource_name = 'index'
        resource_path = ''
    elif path == resource_name:
        resource_path = ''
    else:
        resource_path = path.replace(f'/{resource_name}', '')
    folders = Folder.objects.filter(path=path)
    files = MediaFile.objects.filter(path=path)
    data = list(folders) + list(files)
    context = {'current_path': path, 'current_folder': resource_name, 'parent_folder': resource_path, 'data': data}
    return render(request, 'index.html', context)

@login_required
def upload(request):
    if request.method == 'POST':
        verify_user_directory_existance(request.user.username)
        form = UploadForm(request.POST, request.FILES, username=request.user.username)
        if form.is_valid():
            file = request.FILES['file']
            upload_path = request.POST.get('upload_path')
            username = request.user.username
            file_type = file.content_type.split('/')[0]
            save_file(file, upload_path, username)
            MediaFile.objects.create(
                name=file.name,
                path=upload_path,
                type=file_type,
                size=file.size,
                folder=None,
                creator=request.user,
            )
            if upload_path is '':
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
            username = request.user.username
            create_directory(folder_name, upload_path, username)
            Folder.objects.create(
                name=folder_name,
                path=upload_path,
                parent_folder=None,
                creator=request.user,
            )
            if upload_path is '':
                return redirect('index')
            return redirect('index', path=upload_path)
    else:
        upload_path = request.GET.get('upload_path', '')
        form = CreateFolderForm(initial={'upload_path': upload_path})
    return render(request, 'create_folder.html', {'form': form})