from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentsConfig(AppConfig):
    """Documents app config."""

    name = "software_challenge_api.documents"
    verbose_name = _("Documents")
