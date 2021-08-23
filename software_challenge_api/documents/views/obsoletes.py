"""Documents views."""

# Django REST Framework
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import get_object_or_404

# Serializers
from software_challenge_api.documents.serializers import DocumentModelSerializer

# Models
from software_challenge_api.documents.models import Document
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ObsoleteViewSet(
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """Document view set."""

    serializer_class = DocumentModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Document.objects.filter(
            state='obsolete',
            parent=None
        )

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(ObsoleteViewSet, self).retrieve(request, *args, **kwargs)
        instance = self.get_object()
        documents = Document.objects.filter(
            state='obsolete',
            parent=instance.id
        )
        data = {
            'document': response.data,
            'childs': DocumentModelSerializer(documents, many=True).data
        }
        response.data = data
        return response
