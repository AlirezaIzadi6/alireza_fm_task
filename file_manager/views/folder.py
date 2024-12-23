from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Constants:
from file_manager.constants.directory import UPLOADS_FOLDER, THUMBNAILS_FOLDER
# Data access:
from file_manager.data_access_helpers.folder import get_folder_by_path
# forms:
from file_manager.forms.create_folder import CreateFolderForm
#models:
from file_manager.models import Folder
# utils:
from file_manager.utils.file_processor import read_file, verify_directory_existance, delete_folder
from file_manager.utils.formatting import format_folder_info
from file_manager.utils.path import get_directory_path
# Views:
from file_manager.views.rest_responses import *

@login_required
def create_folder(request):
    if request.method == 'POST':
        user_folder = get_directory_path(UPLOADS_FOLDER, request.user.username, '')
        verify_directory_existance(user_folder)
        form = CreateFolderForm(request.POST, username=request.user.username)
        if form.is_valid():
            folder_name = form.cleaned_data['name']
            upload_path = form.cleaned_data['upload_path']
            username = request.user.username
            parent_folder = get_folder_by_path(upload_path, request.user)
            folder_path = get_directory_path(UPLOADS_FOLDER, username, upload_path+'/'+folder_name)
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
def get_folder_thumbnail(request):
    file_path = 'file_manager/static_files/folder.jpg'
    file_content = read_file(file_path)
    response = HttpResponse(file_content, content_type='image/jpeg')
    return response

@login_required
def get_folder_details(request, id):
    try:
        folder = Folder.objects.get(id=id, creator=request.user)
    except Folder.DoesNotExist:
        return RestHttpResponseNotFound('Folder not found')
    formatted_info = format_folder_info(folder)
    return HttpResponse(formatted_info)

@login_required
def delete_folder_view(request, id):
    try:
        folder_object = Folder.objects.get(id=id, creator=request.user)
    except Folder.DoesNotExist:
        return RestHttpResponseNotFound('Folder not found or not accessible')
    folder_path = get_directory_path(UPLOADS_FOLDER, request.user.username, folder_object.path+'/'+folder_object.name)
    thumbnail_path = get_directory_path(THUMBNAILS_FOLDER, request.user.username, folder_object.path+'/'+folder_object.name)
    folder_object.delete()
    delete_folder(folder_path)
    delete_folder(thumbnail_path)
    return RestHttpResponseSuccess()
