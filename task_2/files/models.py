from django.core.exceptions import ValidationError
from django.db import models

from files.utils import upload_to


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_to, blank=True, null=True)
    file_binary = models.BinaryField(blank=True, null=True)
    storage_type = models.CharField(max_length=4, choices=(('disk', 'Disk'), ('db', 'DB')))

    def clean(self):
        if not self.file and not self.file_binary:
            raise ValidationError('One of the fields "file" or "file_binary" must be filled.')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)