from django.urls import path
from files.views import FileUploadAPIView, FileListAPIView, FileDeleteAPIView, FileDownloadAPIView, LogOperationListAPIView

urlpatterns = [
    path("upload/", FileUploadAPIView.as_view(), name="file-upload"),
    path("list/", FileListAPIView.as_view(), name="file-list"),
    path("delete/<uuid:file_id>/", FileDeleteAPIView.as_view(), name="file-delete"),
    path("download/<uuid:file_id>/", FileDownloadAPIView.as_view(), name="file-download"),
    path('logs/', LogOperationListAPIView.as_view(), name='list-logs'),
]
