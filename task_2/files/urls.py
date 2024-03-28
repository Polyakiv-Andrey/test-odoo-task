from django.urls import path

from files.views import FileListView, FileUploadView, FileDeleteView

urlpatterns = [
    path("", FileListView.as_view(), name="files"),
    path("file-upload/", FileUploadView.as_view(), name="file-upload"),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),
]

app_name = "files"
