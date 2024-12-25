import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
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
import file_manager.utils.file_processor as file_processor
from file_manager.utils.formatting import format_file_info
from file_manager.utils.media_tools.image_processor import create_image_thumbnail, get_image_dimensions
from file_manager.utils.media_tools.video_processor import create_video_thumbnail, get_video_dimensions
from file_manager.utils.path import get_file_path, get_directory_path
# Validators:
from file_manager.validators.path import validate_file_name
# Views:
from file_manager.views.rest_responses import *

@login_required
def upload(request):
    if request.method == 'POST':
        user_folder = get_directory_path(UPLOADS_FOLDER, request.user.username, '')
        file_processor.verify_directory_existance(user_folder)
        form = UploadForm(request.POST, request.FILES, username=request.user.username)
        if form.is_valid():
            file = form.cleaned_data['file']
            upload_path = form.cleaned_data['upload_path']
            parent_folder = get_folder_by_path(upload_path, request.user)
            username = request.user.username
            save_path    = get_directory_path(UPLOADS_FOLDER, username, upload_path)
            file_processor.save_file(file, save_path)
            thumbnail_path = get_directory_path(THUMBNAILS_FOLDER, username, upload_path)
            file_path = save_path+'/'+file.name
            if 'image' in file.content_type:
                width, height = get_image_dimensions(file_path)
                length = 0
                create_image_thumbnail(file.name, save_path, thumbnail_path)
            else:
                length, height, width = get_video_dimensions(file_path)
                create_video_thumbnail(file.name, save_path, thumbnail_path)
            MediaFile.objects.create(
                name=file.name,
                path=upload_path,
                type=file.content_type,
                size=file.size,
                height=height,
                width=width,
                length=length,
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
        file_content = file_processor.read_file(file_path)
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
def rename_file(request, id):
    try:
        new_name = request.POST.get('newName')
        validate_file_name(new_name)
        file = MediaFile.objects.get(id=id, creator=request.user)
        old_name = file.name
        old_extension = os.path.splitext(old_name)[1]
        new_extension = os.path.splitext(new_name)[1]
        if new_extension != old_extension:
            return HttpResponseBadRequest('Changing file extension is not allowed.')
        file_path = get_directory_path(UPLOADS_FOLDER, request.user.username, file.path)
        thumbnail_path = get_directory_path(THUMBNAILS_FOLDER, request.user.username, file.path)
        file_processor.rename(file_path, old_name, new_name)
        file_processor.rename(thumbnail_path, old_name+'.jpg', new_name+'.jpg')
        file.name = new_name
        file.update_date = datetime.now()
        file.save()
        return RestHttpResponseSuccess()
    except MediaFile.DoesNotExist:
        return HttpResponseBadRequest('Invalid id')
    except ValidationError:
        return HttpResponseBadRequest(f'Invalid name')
    except KeyError:
        return HttpResponseBadRequest('Missing arguments')
    except Exception as ex:
        file_processor.rename(file_path, new_name, old_name)
        file_processor.rename(THUMBNAILS_FOLDER, new_name+'.jpg', old_name+'.jpg')
        raise ex

@login_required
def delete_file_view(request, id):
    try:
        file_object = MediaFile.objects.get(id=id, creator=request.user)
    except MediaFile.DoesNotExist:
        return RestHttpResponseNotFound('File not found or not accessible')
    file_path = get_file_path(UPLOADS_FOLDER, request.user.username, file_object.path, file_object.name)
    thumbnail_path = get_file_path(THUMBNAILS_FOLDER, request.user.username, file_object.path, file_object.name+'.jpg')
    file_object.delete()
    file_processor.delete_file(file_path)
    file_processor.delete_file(thumbnail_path)
    return RestHttpResponseSuccess()
