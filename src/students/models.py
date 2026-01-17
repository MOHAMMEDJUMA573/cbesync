from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date
import uuid

from accounts.models import CustomUser
from schools.models import SchoolProfile


def generate_unique_student_id():
    while True:
        new_id = f"STD-{uuid.uuid4().hex[:16].upper()}"
        if not StudentProfile.objects.filter(student_id=new_id).exists():
            return new_id


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    student_id = models.CharField(
        max_length=25,
        unique=True,
        db_index=True,
        default=generate_unique_student_id,
        editable=False
    )

    student_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="students"
    )

    student_admission_number = models.CharField(max_length=30, default="XXXXX")
    student_assessment_number = models.CharField(max_length=20, default="XXXXX")

    student_first_name = models.CharField(max_length=100)
    student_middle_name = models.CharField(max_length=100, blank=True)
    student_last_name = models.CharField(max_length=100)

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    student_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )

    student_dob = models.DateField(default=date(2000, 1, 1))

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

    student_creation_date = models.DateTimeField(auto_now_add=True)
    student_update = models.DateTimeField(auto_now=True)
    student_enrollment_date = models.DateTimeField(auto_now_add=True)

    def student_age(self):
        f_status = "sometimelater"

    def save(self, *args, **kwargs):
        new_user = CustomUser.objects.create_user(
            username=self.student_id.lower(),
            email=self.student_email,
            user_type='student'
        )
        new_user.set_password(self.student_id)
        new_user.save()
        self.user = new_user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name} ({self.student_admission_number})"
