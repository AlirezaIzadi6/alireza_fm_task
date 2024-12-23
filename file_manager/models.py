from django.db import models

from accounts.models import CustomUser

class Folder(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

class MediaFile(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    size = models.IntegerField()
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    parent_folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
