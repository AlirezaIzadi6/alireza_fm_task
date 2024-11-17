from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from file_manager.forms.upload import UploadForm
from file_manager.utils.file_processor import file_processor

@login_required
def index(request):
    return render(request, 'index.html', {'context': {}})

def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        file = request.FILES['file']
        print(file.name)
        print(file.size)
        print(file.content_type)
        if form.is_valid():
            form.save()
            file_processor(file)
            return redirect('index')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})