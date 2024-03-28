import os

from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from file_storage import settings
from files.forms import FileUploadForm
from files.models import File


class FileListView(generic.ListView):
    model = File
    template_name = 'files/files.html'
    context_object_name = 'files'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
        return queryset.order_by("id")


class FileUploadView(generic.CreateView):
    model = File
    form_class = FileUploadForm
    template_name = 'files/file_upload.html'
    success_url = reverse_lazy('files:files')


class FileDeleteView(generic.DeleteView):
    model = File
    success_url = reverse_lazy('files:files')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.storage_type == 'disk':
            file_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return super(FileDeleteView, self).delete(request, *args, **kwargs)
