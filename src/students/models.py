from django.db import models
from datetime import date
import uuid
from schools.models import SchoolProfile
from pathlib import Path
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from accounts.models import CustomUser
from schools.models import SchoolProfile


def generate_unique_student_id():
    while True:
        new_id = f"STD-{uuid.uuid4().hex[:16].upper()}"
        if not StudentProfile.objects.filter(student_id=new_id).exists():
            return new_id

#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"stprf/{fname}{ext}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    student_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_student_id,
        db_index=True,
        editable=False
    )

    student_pic = models.ImageField(
        upload_to=image_file_upload_handler,
        null=True,
        blank=True
    )
    student_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="students",
        null=True
    )

    student_admission_number = models.CharField(
        max_length=30,
        default="XXXXX"
    )
    student_assessment_number = models.CharField(
        max_length=20,
        default="XXXXX"
    )

    student_first_name = models.CharField(
        max_length=100
    )
    student_middle_name = models.CharField(
        max_length=100,
        blank=True
    )
    student_last_name = models.CharField(
        max_length=100
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    student_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
    student_dob = models.DateField(
        default=date(2000, 1, 1)
    )
    ALLERGY_CHOICES = (
        ("ENV","Environment"),
        ("FOD","Food"),
        ("LTX", "Latex"),
        ("IST", "Insects")
    )
    student_allergies = ArrayField(
        models.CharField(max_length=3, choices=ALLERGY_CHOICES),
        blank=True,
        default=list
    )
    BLOOD_GROUPS=(
        ("A", "A"),
        ("B","B"),
        ("AB", "AB"),
        ("O","O")
    )
    student_blood_group = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    ) 
    SP_NEEDS_OPTS=(
        ("T", "Yes"),
        ("F", "No")
    )
    student_s_needs= models.CharField(
        choices=SP_NEEDS_OPTS,
        max_length=1,
        blank=True,
        null=True
    )
    student_e_notes = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    student_email = models.EmailField(
        max_length=100,
        null=True,
        blank=True
    )
    student_home_address = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Student address of residence"
    )
    student_e_contact = PhoneNumberField(
        blank=True,
        help_text="emergency contact"
    )

    STATUS_CHOICES = [
        ('A', 'Active'),
        ('T', 'Transferred'),
        ('G', 'Graduated'),
        ('S', 'Suspended'),
    ]
    student_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    student_admission_date = models.DateTimeField(auto_now_add=True)
    student_update = models.DateTimeField(auto_now=True)
    student_enrollment_date = models.DateTimeField(auto_now_add=True)

    def student_age(self):
        f_status = "sometimelater"

    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name} ({self.student_admission_number})"
