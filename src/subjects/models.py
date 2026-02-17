from django.db import models
import uuid
from classes.models import ClassProfile
from schools.models import SchoolProfile
from classes.models import ProgramProfile
from teachers.models import TeacherProfile
from accounts.models import table_exists


def generate_unique_subject_pkey():
    table_name = "subjects_SubjectProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not SubjectProfile.objects.filter(subject_id=new_id).exists():
                return new_id
    return uuid.uuid4()


class SubjectProfile(models.Model):
    subject_id = models.UUIDField(
        primary_key=True,
        default=generate_unique_subject_pkey,
        editable=False
    )
    subject_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="subject_profiles"
    )
    subject_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE,
        related_name="subject_profiles"
    )
    subject_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subject_profiles"
    )
    subject_code = models.CharField(
        max_length=15,
    )
    subject_name = models.CharField(
        max_length=35,
    )
    subject_program = models.ForeignKey(
        ProgramProfile,
        on_delete=models.CASCADE,
        related_name="subject_profiles"
    )
    subject_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    subject_update_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.subject_name} --- {self.subject_code} --- {self.subject_program}"
