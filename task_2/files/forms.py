from django import forms
from files.models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'storage_type']

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = True
        self.fields['storage_type'].required = True

    def save(self, commit=True):
        file_instance = super(FileUploadForm, self).save(commit=False)
        if file_instance.storage_type == 'db':
            if self.cleaned_data['file']:
                file_instance.file_binary = self.cleaned_data['file'].read()
                file_instance.file = None
        if commit:
            file_instance.save()
        return file_instance

