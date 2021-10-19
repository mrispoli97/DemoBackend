from django.contrib import admin
from django.urls import path
from .views import upload, classify, obfuscate, get_uploaded_files

urlpatterns = [
    path('upload', upload),
    path('classify', classify),
    path('obfuscate', obfuscate),
    path('get-uploaded-files', get_uploaded_files),
]
