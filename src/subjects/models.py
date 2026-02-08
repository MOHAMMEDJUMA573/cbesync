from django.db import models
import uuid
from classes.models import ClassProfile
from schools.models import SchoolProfile
from teachers.models import TeacherProfile
from students.models import StudentProfile


def generate_unique_subject_id():
    while True:
        new_id = f"SBJ-{uuid.uuid4().hex[:16].upper()}"
        if not SubjectProfile.objects.filter(subject_id=new_id).exists():
            return new_id


class SubjectProfile(models.Model):
    subject_name = models.CharField(
        max_length=35,
        default="",
    )
    subject_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_subject_id,
        editable=False
    )
    subject_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE,
        related_name="subject_profiles",
    )
    subject_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="subject_profiles"
    )
    subject_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="subject_profiles"
    )
    STATUS_CHOICES = [
        ('A', 'Active'),
        ('D', 'Dropped'),
        ('S', 'Suspended'),
    ]
    subject_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    subject_creation_date = models.DateTimeField(
        auto_now=True
    )
    subject_update_date = models.DateTimeField(
        auto_now_add=True
    )

    def get_students_objs(self):
        students_class = self.subject_class
        return StudentProfile.objects.filter(student_class=students_class)

    def __str__(self):
        return f"{self.subject_name}  {self.subject_id}"
