from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import StudentProfile
from django.db.models import F

@receiver(post_delete, sender=StudentProfile)
def delete_user_when_student_deleted(sender, instance, **kwargs):    
    #delete user
    if instance.user:
        instance.user.delete()