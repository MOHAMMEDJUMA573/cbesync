from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import StudentProfile
from django.db.models import F

@receiver(post_delete, sender=StudentProfile)
def delete_user_when_student_deleted(sender, instance, **kwargs):
    #eject from the school polpulation
    initial_student_school = instance.student_school
    if initial_student_school:
        initial_student_school.school_students_polpulation = F(
            'school_students_polpulation'
        ) -1
        initial_student_school.save(update_fields=['school_students_polpulation'])

    #delete user
    if instance.user:
        instance.user.delete()