from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect

# data access:
from file_manager.data_access.folder import get_folder_by_path
from file_manager.data_access.file_or_folder import get_file_or_folder
# forms:
from file_manager.forms.create_folder import CreateFolderForm
from file_manager.forms.upload import UploadForm
# mappers
from file_manager.mappers.path import Resource
# models:
from file_manager.models import Folder, MediaFile
#utils:
from file_manager.utils.file_processor import *
from file_manager.utils.file_validator import path_is_valid
from file_manager.utils.formatting import format_folder_info, format_file_info
from file_manager.utils.image_processor import create_image_thumbnail, create_video_thumbnail
from file_manager.utils.path import extract_upper_folders, get_directory_path, get_file_path

@login_required
def index(request, path=''):
    is_thumbnail_request = request.GET.get('thumbnail', False)
    if is_thumbnail_request:
        is_folder_thumbnail_request = request.GET.get('for_folder', False)
        if is_folder_thumbnail_request:
            file_path = 'file_manager/static_files/folder.jpg'
        else:
            resource = Resource(path)
            file_path = get_file_path('thumbnails', request.user.username, resource.path, resource.name)
        file_content = read_file(file_path)
        if file_content is None:
            return HttpResponseNotFound('Not found')
        response = HttpResponse(file_content, content_type='image/jpeg')
        return response
    if not path_is_valid(path):
        return redirect('index')
    resource = Resource(path)
    file_or_folder = get_file_or_folder(resource)
    if path != '' and file_or_folder is None:
        return redirect('index')
    if path == '' or file_or_folder.resource_type == 'folder':
        if path == '':
            current_folder = None
        else:
            current_folder = file_or_folder.resource
        folders = Folder.objects.filter(path=path, creator=request.user)
        files = MediaFile.objects.filter(path=path, creator=request.user)
        upper_folders = extract_upper_folders(current_folder)
        data = []
        for f in folders:
            new_item = {
                'id': f.id,
                'name': f.name,
                'path': f.path,
                'create_date': f.create_date,
                'update_date': f.update_date,
                'resource_type': 'folder',
            }
            data.append(new_item)
        for f in files:
            new_item = {
                'id': f.id,
                'name': f.name,
                'path': f.path,
                'type': f.type,
                'size': f.size,
                'create_date': f.create_date,
                'update_date': f.update_date,
                'resource_type': 'file',
            }
            data.append(new_item)
        context = {'current_path': path, 'current_folder': resource.name, 'parent_folder': resource.path, 'data': data, 'upper_folders': upper_folders}
        return render(request, 'index.html', context)
    elif file_or_folder.resource_type == 'file':
        resource = Resource(path)
        file_path = get_file_path('uploads', request.user.username, resource.path, resource.name)
        file_content = read_file(file_path)
        response = HttpResponse(file_content, content_type=file_or_folder.resource.type)
        return response
    else:
        return redirect('index')

@login_required
def upload(request):
    if request.method == 'POST':
        user_folder = get_directory_path('uploads', request.user.username, '')
        verify_directory_existance(user_folder)
        form = UploadForm(request.POST, request.FILES, username=request.user.username)
        if form.is_valid():
            file = request.FILES['file']
            upload_path = request.POST.get('upload_path')
            parent_folder = get_folder_by_path(upload_path, request.user)
            username = request.user.username
            file_type = file.content_type.split('/')[0]
            save_path = get_directory_path('uploads', username, upload_path)
            save_file(file, save_path)
            thumbnail_path = get_directory_path('thumbnails', username, upload_path)
            if file_type == 'image':
                create_image_thumbnail(file.name, save_path, thumbnail_path)
            else:
                create_video_thumbnail(file.name, save_path, thumbnail_path)
            MediaFile.objects.create(
                name=file.name,
                path=upload_path,
                type=file.content_type,
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
        user_folder = get_directory_path('uploads', request.user.username, '')
        verify_directory_existance(user_folder)
        form = CreateFolderForm(request.POST, username=request.user.username)
        if form.is_valid():
            folder_name = form.cleaned_data['name']
            upload_path = form.cleaned_data['upload_path']
            username = request.user.username
            parent_folder = get_folder_by_path(upload_path, request.user)
            folder_path = get_directory_path('uploads', username, upload_path+'/'+folder_name)
            verify_directory_existance(folder_path)
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

@login_required
def delete_folder_view(request):
    request_id = request.POST.get('id', None);
    if request_id is None or not request_id.isdigit():
        return HttpResponseBadRequest('Invalid ID')
    folder_id = int(request_id)
    try:
        folder_object = Folder.objects.get(id=folder_id, creator=request.user)
        folder_path = get_directory_path('uploads', request.user.username, folder_object.path+'/'+folder_object.name)
        thumbnail_path = get_directory_path('thumbnails', request.user.username, folder_object.path+'/'+folder_object.name)
        folder_object.delete()
        delete_folder(folder_path)
        delete_folder(thumbnail_path)
        return HttpResponse({})
    except Folder.DoesNotExist:
        return HttpResponseNotFound('Folder not found or not accessible')

@login_required
def delete_file_view(request):
    request_id = request.POST.get('id', None);
    if request_id is None or not request_id.isdigit():
        return HttpResponseBadRequest('Invalid ID')
    file_id = int(request_id)
    try:
        file_object = MediaFile.objects.get(id=file_id, creator=request.user)
        file_path = get_file_path('uploads', request.user.username, file_object.path, file_object.name)
        thumbnail_path = get_file_path('thumbnails', request.user.username, file_object.path, file_object.name+'.jpg')
        file_object.delete()
        delete_file(file_path)
        delete_file(thumbnail_path)
        return HttpResponse({})
    except MediaFile.DoesNotExist:
        return HttpResponseNotFound('File not found or not accessible')

@login_required
def get_detail(request):
    resource_id = request.GET.get('id', None)
    resource_type = request.GET.get('type', None)
    if resource_id is None or resource_type is None:
        return HttpResponseBadRequest('Invalid request')
    if resource_type not in ['folder', 'file']:
        return HttpResponseBadRequest('Invalid request')
    if not resource_id.isdigit():
        return HttpResponseBadRequest('Invalid request')
    resource_id = int(resource_id)
    try:
        if resource_type == 'folder':
            folder = Folder.objects.get(id=resource_id, creator=request.user)
            formatted_info = format_folder_info(folder)
        elif resource_type == 'file':
            file = MediaFile.objects.get(id=resource_id, creator=request.user)
            formatted_info = format_file_info(file)
        return HttpResponse(formatted_info)
    except Folder.DoesNotExist:
        return HttpResponseNotFound('Folder not found')
    except MediaFile.DoesNotExist:
        return HttpResponseNotFound('File not found')