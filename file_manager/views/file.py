from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Constants:
from file_manager.constants.directory import UPLOADS_FOLDER, THUMBNAILS_FOLDER
# Data access:
from file_manager.data_access_helpers.folder import get_folder_by_path
# forms:
from file_manager.forms.upload import UploadForm
#models:
from file_manager.models import MediaFile
# utils:
from file_manager.utils.file_processor import save_file, read_file, verify_directory_existance, delete_file
from file_manager.utils.formatting import format_file_info
from file_manager.utils.image_processor import create_image_thumbnail, create_video_thumbnail
from file_manager.utils.path import get_file_path, get_directory_path
# Views:
from file_manager.views.rest_responses import *

@login_required
def upload(request):
    if request.method == 'POST':
        user_folder = get_directory_path(UPLOADS_FOLDER, request.user.username, '')
        verify_directory_existance(user_folder)
        form = UploadForm(request.POST, request.FILES, username=request.user.username)
        if form.is_valid():
            file = form.cleaned_data['file']
            upload_path = form.cleaned_data['upload_path']
            parent_folder = get_folder_by_path(upload_path, request.user)
            username = request.user.username
            save_path    = get_directory_path(UPLOADS_FOLDER, username, upload_path)
            save_file(file, save_path)
            thumbnail_path = get_directory_path(THUMBNAILS_FOLDER, username, upload_path)
            if 'image' in file.content_type:
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
def get_file_thumbnail(request, id: int):
    try:
        file_object = MediaFile.objects.get(id=id, creator=request.user)
        file_path = get_file_path(THUMBNAILS_FOLDER, request.user.username, file_object.path, file_object.name+'.jpg')
        file_content = read_file(file_path)
    except MediaFile.DoesNotExist:
        return HttpResponseNotFound('Not found or not accessible')
    response = HttpResponse(file_content, content_type='image/jpeg')
    return response

@login_required
def get_file_details(request, id):
    try:
        file = MediaFile.objects.get(id=id, creator=request.user)
    except MediaFile.DoesNotExist:
        return RestHttpResponseNotFound('File not found')
    formatted_info = format_file_info(file)
    return HttpResponse(formatted_info)


@login_required
def delete_file_view(request, id):
    try:
        file_object = MediaFile.objects.get(id=id, creator=request.user)
    except MediaFile.DoesNotExist:
        return RestHttpResponseNotFound('File not found or not accessible')
    file_path = get_file_path(UPLOADS_FOLDER, request.user.username, file_object.path, file_object.name)
    thumbnail_path = get_file_path(THUMBNAILS_FOLDER, request.user.username, file_object.path, file_object.name+'.jpg')
    file_object.delete()
    delete_file(file_path)
    delete_file(thumbnail_path)
    return RestHttpResponseSuccess()