"""Documents serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from software_challenge_api.documents.models import Document


class DocumentModelSerializer(serializers.ModelSerializer):
    """Document model serializer."""
    name = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""

        model = Document
        fields = (
            'id',
            'name',
            'file',
            'file_type',
            'state',
            'childs',
        )

    def get_name(self, obj):
        file_name = ''
        if obj.file and hasattr(obj.file, 'name'):
            file_name = obj.file.name
        return file_name

    def get_file_type(self, obj):
        file_name = obj.file.name
        return file_name.split('.')[-1]
