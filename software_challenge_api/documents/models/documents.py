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

    file = models.FileField(upload_to=get_upload_path)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='active')
    childs = models.ManyToManyField('documents.Document', blank=True, null=True, related_name='parent')
