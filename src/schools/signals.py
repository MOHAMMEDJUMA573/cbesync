from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SchoolProfile

@receiver(post_save, sender=SchoolProfile)
def set_username_from_school_id(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        # Set username from school_id
        user.username = str(instance.school_id)
        user.save(update_fields=["username"])
        # Set school_email from user's email
        instance.school_email = user.email
        instance.save(update_fields=["school_email"])