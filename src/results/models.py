from django.db import models
import uuid
from classes.models import ClassProfile
from schools.models import SchoolProfile
from teachers.models import TeacherProfile
from students.models import StudentProfile
from subjects.models import SubjectProfile
from django.core.validators import MaxValueValidator, MinValueValidator



def generate_unique_result_id():
    while True:
        new_id = uuid.uuid4().hex
        if not ResultsProfile.objects.filter(result_id=new_id).exists():
            return new_id


class ResultsProfile(models.Model):
    result_id = models.CharField(
        max_length=32,
        unique=True,
        default=generate_unique_result_id,
        editable=False
    )
    result_student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="results_profile"
    )
    result_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE,
        related_name="results_profile"
    )
    result_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        related_name="results_profile",
        null=True
    )
    result_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="results_profile"
    )
    result_subject = models.ForeignKey(
        SubjectProfile,
        on_delete=models.SET_NULL,
        null=True
    )
    result_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(60), MinValueValidator(0)],
    )
    RESULT_TERM_CHOICES = [
        ("T 1", "Term 1"),
        ("T 2", "Term 2"),
        ("T 3", "Term 3")
    ]
    result_term = models.CharField(
        choices=RESULT_TERM_CHOICES
    )
    result_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    result_update_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.result_student} --- {self.result_score}  --- {self.result_subject}"
