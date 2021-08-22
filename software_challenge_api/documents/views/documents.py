"""Documents views."""

# Django REST Framework
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
# Serializers
from software_challenge_api.documents.serializers import DocumentModelSerializer

# Models
from software_challenge_api.documents.models import Document
from rest_framework.response import Response

class DocumentViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """Document view set."""

    serializer_class = DocumentModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """Return aircraft members."""
        return Document.objects.filter(
            ~Q(state='obsolete'),
        )

    def perform_destroy(self, instance):
        # TODO: Get childs and change state to Obsolete
        instance.state = 'obsolete'
        instance.name += '_OBSOLETE'
        if instance.file:
            new_name = instance.file.name.split('.')
            new_path = new_name[0] + '_OBSOLETE.' + new_name[-1]

            file_path = new_path.replace('document/', 'obsolete/')
            fs = FileSystemStorage()
            file = fs.save(file_path, instance.file)
            instance.file = file
        instance.save()

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = DocumentModelSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        if document.file_type == 'file':
            document.name = document.file.name.split('/')[-1]
        if not document.parent:
            document.parent = document
        document.save()

        data = self.get_serializer(document).data
        return Response(data, status=status.HTTP_201_CREATED)
