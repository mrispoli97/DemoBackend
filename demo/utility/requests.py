import uuid
import os
from django.conf import settings
from pprint import pprint


class Request:

    def __init__(self, request, fields, media):
        pprint(request.data)
        self._request = request
        self._fields = fields
        self._media = media
        self._id = str(uuid.uuid4())

    def get_id(self):
        return self._id

    def _validate(self):
        raise NotImplementedError()

    def get_data(self):
        return self._validate()


class PostRequest(Request):

    def __init__(self, request, fields=[], media=[]):
        self._method = 'POST'
        super(PostRequest, self).__init__(request=request, fields=fields, media=media)

    def _validate(self):
        if self._request.method != self._method:
            raise ValueError(f"Method {self._request.method} invalid. '{self._method}' expected.")
        data = {}
        for field in self._fields:
            if field not in self._request.POST:
                raise ValueError(f"Request invalid, field '{field}' missing.")
            data[field] = self._request.POST[field]

        for field in self._media:
            if field not in self._request.FILES:
                raise ValueError(f"Request invalid, media '{field}' missing.")
            data[field] = self._request.FILES[field]

        return data


class UploadFileRequest(PostRequest):

    def __init__(self, request):
        media = ['file']
        super(UploadFileRequest, self).__init__(request=request, media=media)


class ClassificationRequest(PostRequest):

    def __init__(self, request):
        fields = ['model', 'filepath']
        super(ClassificationRequest, self).__init__(request=request, fields=fields)

    def _validate(self):
        validated_data = PostRequest._validate(self)

        if validated_data['model'] not in ['MobileNet', 'ResNet', 'VGG', 'Xception', 'LightGBM', 'Random Forest',
                                           'XGBoost']:
            raise ValueError(f"model {validated_data['model']} is invalid.")

        return validated_data


class ObfuscationRequest(PostRequest):

    def __init__(self, request):
        fields = ['obfuscation', 'severity', 'filepath']
        super(ObfuscationRequest, self).__init__(request=request, fields=fields)

    def _validate(self):
        validated_data = PostRequest._validate(self)

        if validated_data['obfuscation'] not in ['zeros', 'random', 'junk', 'benign']:
            raise ValueError(f"obfuscation {validated_data['obfuscation']} is invalid.")

        if validated_data['severity'] not in ['0.01', '0.10', '0.25']:
            raise ValueError(f"severity {validated_data['severity']} is invalid.")

        validated_data['dst'] = os.path.join(
            settings.MEDIA_ROOT,
            'workspace',
            validated_data['obfuscation'],
            validated_data['severity']
        )

        if not os.path.exists(validated_data['dst']):
            os.makedirs(validated_data['dst'])

        return validated_data


class GetRequest(Request):

    def __init__(self, request, fields=[], media=[]):
        self._method = 'GET'
        super(GetRequest, self).__init__(request=request, fields=fields, media=media)


class GetUploadedFiles(GetRequest):

    def __init__(self, request):
        super(GetRequest, self).__init__(request)
