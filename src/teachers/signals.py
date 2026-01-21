from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import TeacherProfile
from django.db.models import F

@receiver(post_delete, sender=TeacherProfile)
def delete_user_when_teacher_deleted(sender, instance, **kwargs):
    #eject from the school polpulation
    initial_teacher_school = instance.teacher_school
    if initial_teacher_school:
        initial_teacher_school.school_teachers_polpulation = F(
            'school_teachers_polpulation'
        ) -1
        initial_teacher_school.save(update_fields=['school_teachers_polpulation'])

    #delete user
    if instance.user:
        instance.user.delete()