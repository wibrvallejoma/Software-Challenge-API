"""Documents views."""

# Django REST Framework
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser

# Serializers
from software_challenge_api.documents.serializers import DocumentModelSerializer

# Models
from software_challenge_api.documents.models import Document


class DocumentViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """Document view set."""

    queryset = Document.objects.all()
    serializer_class = DocumentModelSerializer
    parser_classes = (MultiPartParser, FormParser)
