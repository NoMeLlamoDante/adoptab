
from django.contrib import admin
from django.urls import path
from .views import (
    ListPicturesView,
    UploadPictureView,
    DeletePictureView,
    DownloadPictureView
)

urlpatterns = [
    path('upload/', UploadPictureView.as_view(), name="upload-picture"),
    path('list/', ListPicturesView.as_view(), name="list-picture"),
    path('download/<int:id>/',
         DownloadPictureView.as_view(),
         name="download-picture"),
    path('delete/<int:id>/',
         DeletePictureView.as_view(),
         name="delete-picture"),
]
