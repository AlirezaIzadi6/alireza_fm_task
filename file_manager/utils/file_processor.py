import os

def file_processor(file):
    name = file.name
    with open('uploads\\'+name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)