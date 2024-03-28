import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.urls import reverse
from django.core.files.base import ContentFile

from .forms import FileUploadForm
from .models import File
from .views import FileListView


class FileListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.file1 = File.objects.create(name='TestFile1', storage_type='disk', file=self.create_test_file('testfile1.txt'))
        self.file2 = File.objects.create(name='TestFile2', storage_type='disk', file=self.create_test_file('testfile2.txt'))

    def create_test_file(self, name):
        return ContentFile(b'test content', name=name)

    def test_file_list_view(self):
        request = self.factory.get(reverse('files:files'))
        response = FileListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.file1.name)
        self.assertContains(response, self.file2.name)

    def test_search_file_list_view(self):
        request = self.factory.get(reverse('files:files'), {'q': 'TestFile1'})
        response = FileListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.file1.name)
        self.assertNotContains(response, self.file2.name)


class FileUploadViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_file_upload_view(self):
        fake_file = SimpleUploadedFile("test_file.txt", b"file_content")
        response = self.client.post(
            reverse("files:file-upload"),
            {"name": "Test File", "file": fake_file, "storage_type": "db"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(File.objects.filter(name="Test File").exists())


class FileUploadFormTest(TestCase):
    def test_form_valid_with_db_storage(self):
        fake_file = b'test content'
        file_upload = SimpleUploadedFile('test.txt', fake_file)
        form_data = {'name': 'Test File', 'file': file_upload, 'storage_type': 'db'}
        form = FileUploadForm(data=form_data, files={'file': file_upload})

        self.assertTrue(form.is_valid())
        self.assertTrue(form.fields['file'].required)
        self.assertTrue(form.fields['storage_type'].required)
        file_instance = form.save()
        self.assertEqual(file_instance.name, 'Test File')
        self.assertEqual(file_instance.storage_type, 'db')
        self.assertIsNotNone(file_instance.file_binary)


class FileDeleteViewTest(TestCase):
    def setUp(self):
        fake_file = b'test content'
        file_upload = SimpleUploadedFile('test.txt', fake_file)
        self.file = File.objects.create(name='TestFile', storage_type='disk', file=file_upload)

    def test_file_deleted_with_disk_storage(self):
        file_path = self.file.file.path
        response = self.client.post(reverse('files:file-delete', kwargs={'pk': self.file.pk}))
        self.assertFalse(os.path.exists(file_path))

    def test_file_not_deleted_with_db_storage(self):
        fake_file = b'test 2 content'
        file_db = File.objects.create(name='TestFile_DB', storage_type='db', file_binary=fake_file)
        response = self.client.post(reverse('files:file-delete', kwargs={'pk': file_db.pk}))
        self.assertTrue(file_db.file_binary)

    def test_redirect_after_deletion(self):
        response = self.client.post(reverse('files:file-delete', kwargs={'pk': self.file.pk}))
        self.assertRedirects(response, reverse('files:files'))
