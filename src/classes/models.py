from django.db import models
from schools.models import SchoolProfile
from teachers.models import TeacherProfile
import uuid
from pathlib import Path
from django.contrib.postgres.fields import ArrayField
from accounts.models import CustomUser

def generate_unique_class_id():
    while True:
        new_id = f"CLS-{uuid.uuid4().hex[:16].upper()}"
        if not ClassProfile.objects.filter(class_id=new_id).exists():
            return new_id

#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"clsprf/{fname}{ext}"

def generate_unique_programme_id():
    while True:
        new_id = f"PRG-{uuid.uuid4().hex[:16].upper()}"
        if not ProgrammeProfile.objects.filter(programme_id=new_id).exists():
            return new_id
        

class ProgrammeProfile(models.Model):
    programme_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_class_id,
        editable=False
    )
    programme_name = models.CharField(
        max_length=50,
        help_text="The name of the class e.g -stoic-room "
    )
    CLASS_LEVEL_CHOICES = [
        (1, "Grade 1"),(2, "Grade 2"),(3, "Grade 3"),
        (4, "Grade 4"), (5, "Grade 5"), (6, "Grade 6"),
        (7, "Grade 7"), (8, "Grade 8"), (9, " Grade 9"),
        (10, "Grade 10"), (11, "Grade 11"), (12, "Grade 12"),
        (13, "Other")
    ]
    programme_levels = ArrayField(
        models.CharField(max_length=3, choices=CLASS_LEVEL_CHOICES),
        blank=True,
        default=list
    )

class ClassProfile(models.Model):
    class_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_class_id,
        editable=False
    )
    class_name = models.CharField(
        max_length=50,
    )
    class_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="class_profiles",
        null=True
    )

    CLASS_LEVEL_CHOICES = [
        (1, "Grade 1"),(2, "Grade 2"),(3, "Grade 3"),
        (4, "Grade 4"), (5, "Grade 5"), (6, "Grade 6"),
        (7, "Grade 7"), (8, "Grade 8"), (9, " Grade 9"),
        (10, "Grade 10"), (11, "Grade 11"), (12, "Grade 12"),
        (13, "Other")
    ]
    class_level = models.IntegerField(
        choices=CLASS_LEVEL_CHOICES,
        help_text=""
    )
    class_program = models.ForeignKey(
        ProgrammeProfile,
        on_delete=models.CASCADE,
        related_name="class_profiles"
    )
    class_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL, null=True,
        blank=True, related_name='classt_profile',
        help_text="Teache assigned to the class"
    )
    CLASS_STREAM_CHOICES = (
        ("W", "W"),
        ("X", "X"),
        ("Y", "Y"),
        ("Z", "Z"),
    )
    class_stream = models.CharField(
        choices=CLASS_STREAM_CHOICES,
        max_length=1,
    )
    CLASS_STATUS_CHOICES = [
        ('Ac', 'Active'),
        ('Ar', 'Archived'),
    ]
    class_status = models.CharField(
        max_length=2, choices=CLASS_STATUS_CHOICES,
        default='Ac',
    )
    
    class_creation_date = models.DateTimeField(
        auto_now_add=True,
    )
    class_updated_date = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.class_name}-{self.class_level} ({self.class_school.school_name})"

