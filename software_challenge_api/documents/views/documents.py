"""Documents views."""

# Django REST Framework
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers

from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone

# Serializers
from software_challenge_api.documents.serializers import DocumentModelSerializer

# Models
from software_challenge_api.documents.models import Document
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.filter(~Q(state='obsolete'), parent=None)
    serializer_class = DocumentModelSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        document = serializer.save(owner=self.request.user,)
        if document.file and not document.name:
            document.file_type = 'file'
            document.name = document.file.name.split('/')[-1]

        if document.name and not document.file:
            document.file_type = 'folder'

        document.save()

    def get_object(self):
        """Return the aircraft member by using the user's username."""
        return get_object_or_404(
            Document,
            id=self.kwargs['pk'],
            state='active'
        )

    def obsolete_document(self, parent_name, child_instance):
        child_instance.state = 'obsolete'
        child_instance.name += '_OBSOLETE'

        # new_parent_name = parent_name + '_OBSOLETE'

        new_name = child_instance.file.name.split('.')
        new_path = new_name[0] + '_OBSOLETE.' + new_name[-1]

        file_path = new_path.replace('document/', 'obsolete/')
        fs = FileSystemStorage()
        file = fs.save(file_path, child_instance.file)
        child_instance.file = file
        return child_instance

    def perform_destroy(self, instance):
        instance.state = 'obsolete'
        original_name = instance.name
        instance.name += '_OBSOLETE'
        if instance.file_type == 'file':
            if instance.file:
                new_name = instance.file.name.split('.')
                new_path = new_name[0] + '_OBSOLETE.' + new_name[-1]
                file_path = new_path.replace('document/', 'obsolete/')
                fs = FileSystemStorage()
                file = fs.save(file_path, instance.file)
                instance.file = file
        elif instance.file_type == 'folder':
            childs = instance.childs.all()
            # import pdb; pdb.set_trace()
            for child in childs:
                child = self.obsolete_document(original_name, child)
                child.save()
        self.send_delete_notification_email(instance.owner, instance.name)
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(DocumentViewSet, self).retrieve(request, *args, **kwargs)
        instance = self.get_object()
        documents = Document.objects.filter(
            state='active',
            parent=instance.id
        )
        data = {
            'document': response.data,
            'childs': DocumentModelSerializer(documents, many=True).data
        }
        response.data = data
        return response

    def send_delete_notification_email(self, user, document_name):
        """Send notification to given user."""
        subject = f'Hello @{user.username}! Your files are now obsolete.'
        from_email = 'Software Challenge <noreply@api.software_challenge.com>'
        content = render_to_string(
            'emails/users/obsolete_document.html',
            {'document_name': document_name, 'user': user}
        )

        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
