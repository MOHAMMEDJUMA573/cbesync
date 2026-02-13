from django.db import models
import uuid
from datetime import datetime
from classes.models import ClassProfile
from classes.models import ProgramProfile
from schools.models import SchoolProfile
from teachers.models import TeacherProfile
from students.models import StudentProfile
from subjects.models import SubjectProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import table_exists

def generate_unique_subject_pkey():
    table_name = "results_SubjectProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not SubjectProfile.objects.filter(subject_id=new_id).exists():
                return new_id
    return uuid.uuid4()

def generate_unique_result_pkey():
    table_name = "results_ResultsProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not ResultsProfile.objects.filter(result_id=new_id).exists():
                return new_id
    return uuid.uuid4()

class SubjectProfile(models.Model):
    subject_id = models.UUIDField(
        primary_key=True,
        default=generate_unique_subject_pkey,
        editable=False
    )
    subject_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE
    )
    subject_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    subject_code = models.CharField(
        max_length=15,
    )
    subject_name = models.CharField(
        max_length=35,
    )
    subject_program = models.ForeignKey(
        ProgramProfile,
        on_delete=models.CASCADE
    )
    subject_creation_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.subject_name} --- {self.subject_code} --- {self.subject_program}"

class ResultsProfile(models.Model):
    result_id = models.UUIDField(
        primary_key=True,
        default=generate_unique_result_pkey,
        editable=False
    )
    result_student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="result_profiles"
    )
    result_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE,
        related_name="result_profiles"
    )
    result_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        related_name="result_profiles",
        null=True
    )
    result_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="result_profiles"
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
    RESULT_PERIOD_CHOICES = [
        ("Opener", "Opener"),
        ("Mid", "Mid-Term"),
        ("End", "End-Term")
    ]
    result_period = models.CharField(
        choices=RESULT_PERIOD_CHOICES,
        default="Opener"
    )
    result_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(datetime.today().year - 10),
            MaxValueValidator(datetime.today().year + 10)
        ],
        default=int(datetime.today().year)
    )
    result_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    result_update_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.result_student} --- {self.result_score}  --- {self.result_subject}"
