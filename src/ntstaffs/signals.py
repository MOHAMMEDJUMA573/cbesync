from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import NtStaffProfile
from django.db.models import F

@receiver(post_delete, sender=NtStaffProfile)
def delete_user_when_teacher_deleted(sender, instance, **kwargs):
    #eject from the school polpulation
    initial_ntstaff_school = instance.ntstaff_school
    if initial_ntstaff_school:
        initial_ntstaff_school.school_ntstaffs_polpulation = F(
            'school_ntstaffs_polpulation'
        ) -1
        initial_ntstaff_school.save(update_fields=['school_ntstaffs_polpulation'])

    #delete user
    if instance.user:
        instance.user.delete()