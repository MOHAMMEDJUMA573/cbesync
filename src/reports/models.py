from django.db import models
from accounts.models import table_exists
from results.models import ExaminationProfile
from classes.models import ClassProfile
from students.models import StudentProfile
import uuid

def generate_unique_streport_pkey():
    table_name = "reports_StudentEReportProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not StudentEReportProfile.objects.filter(streport_id=new_id).exists():
                return new_id
    return uuid.uuid4()

# Create your models here.
class StudentEReportProfile(models.Model):
    streport_id = models.UUIDField(
        primary_key=True,
        default=generate_unique_streport_pkey,
        editable=False
    )
    streport_examination = models.ForeignKey(
        ExaminationProfile,
        on_delete=models.CASCADE
    )
    streport_class = models.ForeignKey(
        ClassProfile,
        on_delete=models.CASCADE,
        related_name="stereport_profiles"
    )
    streport_student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="stereport_profile"
    )
    streport_t_score = models.IntegerField(
        default=0
    )
    streport_points_score = models.IntegerField(
        default=0
    )
    streport_c_position = models.IntegerField(
        default=0
    )
    streport_a_grade = models.CharField(
        max_length=5,
        default="EE1"
    )
    streport_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    streport_update_date = models.DateTimeField(
        auto_now=True
    )
    streport_p_level = models.CharField(
        default="",
        max_length=5
    )    

    def __str__(self):
        return f"{self.streport_student.student_full_name} {self.streport_examination.exam_short_description()}"