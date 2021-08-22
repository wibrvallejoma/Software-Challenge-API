"""Document model."""

import os

# Django
from django.db import models

# Utilities
from software_challenge_api.utils.models import BaseModel


def get_upload_path(instance, filename):
    return os.path.join(
      "document/", filename)


class Document(BaseModel):
    """Document model.

    A document holds name, path, type an possible childs.
    """
    FILE_CHOICES = [
        ('file', 'File'),
        ('folder', 'Folder')
    ]
    STATE_CHOICES = [
        ('active', 'active'),
        ('obsolete', 'obsolete')
    ]

    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    state = models.CharField(max_length=25, choices=STATE_CHOICES, default='active')
    file_type = models.CharField(max_length=25, choices=FILE_CHOICES, default='file')
    childs = models.ManyToManyField('documents.Document', related_name='doc_childs', blank=True, null=True)
    parent = models.ForeignKey('documents.Document', blank=True, null=True, on_delete=models.CASCADE, related_name='doc_parent')
