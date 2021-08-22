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
        )
