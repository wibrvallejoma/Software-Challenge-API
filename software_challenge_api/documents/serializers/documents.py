"""Documents serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from software_challenge_api.documents.models import Document


class DocumentModelSerializer(serializers.ModelSerializer):
    """Document model serializer."""
    # file_name = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""

        model = Document
        fields = (
            'id',
            'name',
            'file',
            'file_type',
            'state',
            'parent',
            'childs'
        )

    # def get_file_name(self, obj):
    #     file_name = ''
    #     if obj.file and hasattr(obj.file, 'name'):
    #         file_name = obj.file.name
    #     return file_name
