from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import ParentProfile
from django.db.models import F

@receiver(post_delete, sender=ParentProfile)
def delete_user_when_teacher_deleted(sender, instance, **kwargs):
    #eject from the school polpulation
    initial_parent_school = instance.parent_school
    if initial_parent_school:
        initial_parent_school.school_parents_polpulation = F(
            'school_parents_polpulation'
        ) -1
        initial_parent_school.save(update_fields=['school_parents_polpulation'])

    #delete user
    if instance.user:
        instance.user.delete()