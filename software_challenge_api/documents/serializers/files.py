"""Documents serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from software_challenge_api.documents.models import Document


class CreateFileSerializer(serializers.Serializer):
    """Document model serializer."""
    name = serializers.CharField(max_length=255)
    file = serializers.FileField(max_length=None, allow_empty_file=False)
    parent = serializers.PrimaryKeyRelatedField(queryset=Document.objects.filter(file_type='folder'))

    def create(self, data):
        print(data.__dict__)
        document = Document.objects.create(**data, file_type='file')
        return document
