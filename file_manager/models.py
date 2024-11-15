from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

class MediaFile(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    type = models.CharField(max_length=5)
    size = models.IntegerField()
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)