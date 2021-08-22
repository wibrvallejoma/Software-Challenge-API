"""API URLs."""

# Django
from django.conf import settings

# REST Framework
from rest_framework.routers import DefaultRouter, SimpleRouter

# Views
from software_challenge_api.users.views import users as user_views
from software_challenge_api.documents.views import documents as document_views
from software_challenge_api.documents.views import obsoletes as obsolete_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'users', user_views.UserViewSet, basename='users')
router.register(r'documents', document_views.DocumentViewSet, basename='documents')
router.register(r'obsoletes', obsolete_views.ObsoleteViewSet, basename='obsoletes')


app_name = "api"
urlpatterns = router.urls
