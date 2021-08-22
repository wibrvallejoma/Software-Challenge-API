"""Document Signals"""

# Django
from django.dispatch import receiver
from django.db.models.signals import post_save

from software_challenge_api.users.models import User, Profile

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    """
    Django signal that creates a profile as default
    when a new user is created (post_save)
    """
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
