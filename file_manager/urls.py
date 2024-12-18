from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('root/', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('details/', views.get_detail, name='details'),
    path('delete/', views.delete_file, name='delete'),
    path('root/<path:path>', views.index, name='index'),
    path('', lambda request: redirect('root/', permanent=True))
]
