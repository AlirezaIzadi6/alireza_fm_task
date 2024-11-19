from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('<path:path>', views.index, name='index'),
]
