from django.db import models
from accounts.models import CustomUser
from schools.models import SchoolProfile
import uuid
from pathlib import Path



def generate_unique_ntstaff_id():
    while True:
        new_id = f"NTS-{uuid.uuid4().hex[:16].upper()}"
        if not NtStaffProfile.objects.filter(ntstaff_id=new_id).exists():
            return new_id
        
#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"ntsprf/{fname}{ext}"

class NtStaffProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="ntstaff_profile"
    )

    ntstaff_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_ntstaff_id,
        db_index=True,
        editable=False
    )

    nststaff_pic = models.ImageField(
        upload_to=image_file_upload_handler,
        null=True,
        blank=True
    )
    nststaff_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="nststaffs",
        null=True
    )

    ntstaff_first_name = models.CharField(
        max_length=35
    )
    ntstaff_middle_name = models.CharField(
        max_length=35,
        blank=True,
        null=True
    )
    ntstaff_last_name = models.CharField(
        max_length=35
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    ntstaff_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
