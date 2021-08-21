"""API URLs."""

# Django
from django.conf import settings

# REST Framework
from rest_framework.routers import DefaultRouter, SimpleRouter

# Views
from software_challenge_api.users.views import users as user_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'users', user_views.UserViewSet, basename='users')


app_name = "api"
urlpatterns = router.urls
