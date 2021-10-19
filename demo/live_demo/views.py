import shutil

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from utility.requests import UploadFileRequest, ClassificationRequest, ObfuscationRequest, GetUploadedFiles
from pprint import pprint
from django.core.files.storage import FileSystemStorage
from utility import utils
from django.conf import settings
import os
from utility.redis import RequestPipeline, ResponseTable
import time

pipeline = RequestPipeline()
table = ResponseTable()


@api_view(['POST'])
def upload(request):
    cr = UploadFileRequest(request=request)
    try:
        data = cr.get_data()
        file = data['file']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'workspace', 'original'))
        filename = fs.save(str(file), file)
        return Response(data=f'File {filename} uploaded successfully.', status=status.HTTP_200_OK)
    except Exception as e:
        message = f"Exception: {e}"
        print(message)
        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def classify(request):
    global pipeline
    global table
    cr = ClassificationRequest(request=request)
    try:
        data = cr.get_data()
        id = cr.get_id()
        pipeline.put({
            'id': id,
            'job': 'classification',
            'data': data,
        })
        while id not in table:
            pass
        prediction = table.get(id)
        table.remove(id)
        print(f"Prediction: {prediction}")
        return Response(data=prediction, status=status.HTTP_200_OK)
    except Exception as e:
        message = f"Exception: {e}"
        print(message)
        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def obfuscate(request):
    global pipeline
    global table
    obr = ObfuscationRequest(request=request)
    try:
        data = obr.get_data()
        id = obr.get_id()
        pipeline.put({
            'id': id,
            'job': 'obfuscation',
            'data': data,
        })
        while id not in table:
            pass
        ob_filepath = table.get(id)
        table.remove(id)
        print(f"Obfuscated file: {ob_filepath}")
        return Response(data=ob_filepath, status=status.HTTP_200_OK)
    except Exception as e:
        message = f"Exception: {e}"
        print(message)
        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_uploaded_files(request):
    try:
        data = {}
        for obfuscation in ['benign', 'junk', 'random', 'zeros']:
            for severity in ['0.01', '0.10', '0.25']:
                path = os.path.join(settings.MEDIA_ROOT, 'workspace', obfuscation, severity)
                if os.path.exists(path) and len(os.listdir(path)) > 0:
                    if obfuscation not in data:
                        data[obfuscation] = {}
                    data[obfuscation][severity] = os.listdir(path)
        if len(os.listdir(os.path.join(settings.MEDIA_ROOT, 'workspace', 'original'))) > 0:
            data['original'] = os.listdir(os.path.join(settings.MEDIA_ROOT, 'workspace', 'original'))
        pprint(data)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        message = f"Exception: {e}"
        print(message)
        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
