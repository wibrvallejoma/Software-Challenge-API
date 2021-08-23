"""Documents serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from software_challenge_api.documents.models import Document
from rest_framework.generics import get_object_or_404


class DocumentModelSerializer(serializers.ModelSerializer):
    """Document model serializer."""
    owner = serializers.StringRelatedField(read_only=True)
    file_type = serializers.CharField(read_only=True)

    class Meta:
        """Meta class."""

        model = Document
        fields = (
            'name',
            'file',
            'parent',
            'childs',
            'id',
            'file_type',
            'state',
            'owner',
            'created',
            'modified',
            'childs'
        )
        read_only_fields = (
            'state', 'owner',
            'file_type',
            'created', 'modified')

    def validate(self, data):
        """Ensure folder does not have file and Files does have file"""
        name = data.get('name', None)
        file = data.get('file', None)

        if name and file:
            raise serializers.ValidationError('If a folder is being created, do not upload a file.')

        if not name and not file:
            raise serializers.ValidationError('Name is required for folders. File is required for Files')

        return data
