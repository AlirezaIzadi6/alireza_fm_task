from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

class RestHttpResponseSuccess(HttpResponse):
    def __init__(self, message = 'ok', *args, **kwargs):
        super().__init__({'message': message}, *args, **kwargs)

class RestHttpResponseBadRequest(HttpResponseBadRequest):
    def __init__(self, message, *args, **kwargs):
        super().__init__({'message': message}, *args, **kwargs)

class RestHttpResponseNotFound(HttpResponseNotFound):
    def __init__(self, message = 'Page not found', *args, **kwargs):
        super().__init__({'message': message}, *args, **kwargs)