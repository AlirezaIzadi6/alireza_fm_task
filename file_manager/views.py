from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from file_manager.forms.upload import UploadForm
from file_manager.utils.file_processor import save_file

@login_required
def index(request):
    return render(request, 'index.html', {'context': {}})

@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, username=request.user.username)
        if form.is_valid():
            file = request.FILES['file']
            upload_path = request.POST.get('upload_path')
            username = request.user.username
            save_file(file, upload_path, username)
            return redirect('index')
    else:
        upload_path = request.GET.get('upload_path', '/')
        form = UploadForm(initial={'upload_path': upload_path})
    return render(request, 'upload.html', {'form': form})