from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('file_manager/', include('file_manager.urls')),
    path('accounts/', include('accounts.urls')),
]
