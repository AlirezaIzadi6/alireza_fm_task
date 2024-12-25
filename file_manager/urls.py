from django.shortcuts import redirect
from django.urls import path
from file_manager.views import index, file, folder

urlpatterns = [
    path('root/', index.index, name='index'),
    path('root/<path:path>', index.index, name='index'),
    path('thumbnails/folder/', folder.get_folder_thumbnail, name='get_folder_thumbnail'),
    path('thumbnails/file/<int:id>', file.get_file_thumbnail, name='get_file_thumbnail'),
    # Create:
    path('upload/', file.upload, name='upload'),
    path('create_folder/', folder.create_folder, name='create_folder'),
    # Retrieve:
    path('details/folder/<int:id>', folder.get_folder_details, name='get_folder_details'),
    path('details/file/<int:id>', file.get_file_details, name='get_file_details'),
    # Update:
    path('rename/folder/<int:id>', folder.rename_folder, name='rename_folder'),
    path('rename/file/<int:id>', file.rename_file, name='rename_file'),
    # Delete:
    path('delete/file/<int:id>', file.delete_file_view, name='delete_file'),
    path('delete/folder/<int:id>', folder.delete_folder_view, name='delete_folder'),

    path('', lambda request: redirect('root/', permanent=True))
]
