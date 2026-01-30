from django.db import models
from accounts.models import CustomUser
from schools.models import SchoolProfile
import uuid
from pathlib import Path
from phonenumber_field.modelfields import PhoneNumberField


def generate_unique_parent_id():
    while True:
        new_id = f"PRT-{uuid.uuid4().hex[:16].upper()}"
        if not ParentProfile.objects.filter(parent_id=new_id).exists():
            return new_id
        
#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"prtprf/{fname}{ext}"

class ParentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="parent_profile"
    )

    parent_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_parent_id,
        editable=False
    )

    parent_pic = models.ImageField(
        upload_to=image_file_upload_handler,
        null=True,
        blank=True
    )
    parent_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="parents",
        null=True
    )

    parent_first_name = models.CharField(
        max_length=35
    )
    parent_middle_name = models.CharField(
        max_length=35,
        blank=True,
        null=True
    )
    parent_last_name = models.CharField(
        max_length=35
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    parent_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
    
    parent_phone = PhoneNumberField(
        help_text="parent contact"
    )
    parent_email = models.EmailField(
        max_length=100,
    )
    parent_home_address = models.CharField(
        max_length=50,
        help_text="parents address of residence"
    )

    STATUS_CHOICES = [
        ('A', 'Active'),
        ('D', 'Done'),
        ('S', 'Suspended'),
        ('R', 'Reported'),
    ]
    parent_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='E'
    )
    
    parent_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    parent_update = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.parent_first_name} {self.parent_last_name} ({self.parent_id})"

    