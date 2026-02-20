from django.db import models
import uuid
from datetime import datetime
from classes.models import ClassProfile
from schools.models import SchoolProfile
from teachers.models import TeacherProfile
from students.models import StudentProfile
from subjects.models import SubjectProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import table_exists

def generate_unique_exam_pkey():
    table_name = "results_ExaminationProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not ExaminationProfile.objects.filter(examination_id=new_id).exists():
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


class ExaminationProfile(models.Model):
    examination_id = models.UUIDField(
        primary_key=True,
        default=generate_unique_exam_pkey,
        editable=False
    )
    examination_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="examination_profiles"
    )
    examination_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE,
        related_name="examination_profiles"
    )
    EXAMINATION_TERM_CHOICES = [
        ("T 1", "Term 1"),
        ("T 2", "Term 2"),
        ("T 3", "Term 3")
    ]
    examination_term = models.CharField(
        choices=EXAMINATION_TERM_CHOICES
    )
    EXAMINATION_PERIOD_CHOICES = [
        ("Opener", "Opener"),
        ("Mid", "Mid-Term"),
        ("End", "End-Term")
    ]
    examination_period = models.CharField(
        choices=EXAMINATION_PERIOD_CHOICES,
        default="Opener"
    )
    examination_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(datetime.today().year - 10),
            MaxValueValidator(datetime.today().year + 10)
        ],
        default=int(datetime.today().year)
    )
    examination_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    examination_update_date = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "examination_school",
                    "examination_class",
                    "examination_term",
                    "examination_period",
                ],
                name="unique_exam_profile_per_context"
            )
        ]

    def exam_short_description(self):
        return f"{self.get_examination_term_display()} - {self.examination_period} - {self.examination_creation_date.year}"
    def __str__(self):
        return f"{self.examination_school.school_name} --- {self.examination_class.class_full_str} --- {self.examination_term}---{self.examination_period}"

class ResultsProfile(models.Model):
    result_id = models.UUIDField(
        primary_key=True,
        default=generate_unique_result_pkey,
        editable=False
    )
    RESULT_STATUS_CHOICES = [
        (0, "new"),
        (1, "updated"),
    ]
    result_status = models.CharField(
        choices=RESULT_STATUS_CHOICES,
        default=0
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
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    result_examination = models.ForeignKey(
        ExaminationProfile,
        on_delete=models.CASCADE,
        related_name="result_profiles",
        null=True
    )
    result_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    result_update_date = models.DateTimeField(
        auto_now=True
    )

    @property
    def result_year(self):
        return self.result_examination.examination_year

    @property
    def result_period(self):
        return self.result_examination.examination_period
   
    @property
    def result_term(self):
        return self.result_examination.examination_term

    def __str__(self):
        return f"{self.result_student} ---{self.result_score}  ---{self.result_subject.subject_name} ---{self.result_examination}"
