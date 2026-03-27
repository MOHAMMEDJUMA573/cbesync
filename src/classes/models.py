from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Rank, DenseRank
from schools.models import SchoolProfile
from teachers.models import TeacherProfile
import uuid
from pathlib import Path
from django.contrib.postgres.fields import ArrayField
from accounts.models import table_exists
from django.core.validators import MaxValueValidator, MinValueValidator

"""
    Thinking of class promotion -> a new class is created with a parent class field pointing to the original class, i.e
    the class with a parent class field of none i.e the one created officially by the school, the prmotion class creates subjects, exams
    and reports based on the levels for each student in the old class then the students are pointed to the promotion class
"""

def generate_unique_class_pkey():
    table_name = "classes_ClassProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not ClassProfile.objects.filter(id=new_id).exists():
                return new_id
    return uuid.uuid4()
              
def generate_unique_class_id():
    table_name = "classes_ClassProfile"
    if table_exists(table_name):
        while True: 
            new_id = f"CLS-{uuid.uuid4().hex[:16].upper()}"       
            if not ClassProfile.objects.filter(class_id=new_id).exists():
                return new_id
    return f"CLS-{uuid.uuid4().hex[:16].upper()}"

#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"clsprf/{fname}{ext}"

def generate_unique_program_pkey():
    table_name = "classes_ProgramProfile"
    if table_exists(table_name):
        while True:
            new_id = uuid.uuid4()
            if not ProgramProfile.objects.filter(id=new_id).exists():
                return new_id
    return uuid.uuid4()

def generate_unique_program_id():
    table_name = "classes_ProgramProfile"
    if table_exists(table_name):
        while True:
            new_id = f"PRG-{uuid.uuid4().hex[:16].upper()}"
            if not ProgramProfile.objects.filter(program_id=new_id).exists():
                return new_id
    return f"PRG-{uuid.uuid4().hex[:16].upper()}"
        
def generate_program_subjects(level):
    CBE_SUBJECTS_DICT = {
        "pre_primary": ["Language Activities", "Mathematical Activities", "Creative Activities", "Environment Activities", "Religious Activities"],
        "upper_primary": ["English", "Kiswahili", "Mathematics", "Intergrated Science", "C.A & Social Studies" ],
        "junior_secondary": ["English", "Kiswahili", "Mathematics", "Religious Education", "Social Studies", "Intergrated Science", "Pretechnical Studies", "Agri. & Nutrition", "C.A & Sports"]
    }
    if level in [1,2,3]:
        return list(CBE_SUBJECTS_DICT["pre_primary"])
    elif level in [4,5,6]:
        return list(CBE_SUBJECTS_DICT["upper_primary"])
    elif level in [7,8,9]:
        return list(CBE_SUBJECTS_DICT["junior_secondary"])

def gen_initial():
    generate_program_subjects(1)

class ProgramProfile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=generate_unique_program_pkey,
        editable=False
    )
    program_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_program_id,
        editable=False
    )
    STARTING_PROGRAMS = [
        ('JSS', 'Junior Secondary'),
        ('UPE', 'Upper Primary'),
        ('LPE', 'Lower Primary'),
        ('PPE', 'Pre Primary'),
        ('OTH', 'Other')
    ]
    program_name = models.CharField(
        choices=STARTING_PROGRAMS
    )
    program_levels = ArrayField(
        models.CharField(max_length=25),
        blank=True,
        default=list
    )
    program_subjects = ArrayField(
        models.CharField(max_length=35),
        blank=True,
        default=gen_initial
    )
    def __str__(self):
        return f"{self.program_id} --- {self.program_name} --- {self.program_levels}"

class ClassProfile(models.Model):
    id = models.UUIDField(
        default=generate_unique_class_pkey,
        primary_key=True,
        editable=False
    )
    class_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_class_id,
        editable=False
    )
    CLASS_TITLES_CHOICES = [
        ("N", "North"),
        ("S", "South"),
        ("W", "West"),
        ("E", "East")
    ]
    class_title = models.CharField(
        max_length=1,
        choices=CLASS_TITLES_CHOICES,
        default="N",
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
        ProgramProfile,
        on_delete=models.CASCADE,
        related_name="class_profiles"
    )
    class_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classt_profiles',
        help_text="Teache assigned to the class"
    )

    class_description = models.CharField(
        null=True,
        blank=True
    )

    CLASS_STATUS_CHOICES = [
        ('Ac', 'Active'),
        ('Ar', 'Archived'),
    ]
    class_status = models.CharField(
        max_length=2, choices=CLASS_STATUS_CHOICES,
        default='Ac',
    )
    class_capacity = models.IntegerField(
        validators=[MaxValueValidator(300), MinValueValidator(50)]
    )
    
    # class_parent = models.ForeignKey(
    #     ClassProfile,
    #     on_delete=models.CASCADE,
    #     related_name="child_class",
    #     null=True,
    #     blank=True
    # )
    class_creation_date = models.DateTimeField(
        auto_now_add=True,
    )
    class_updated_date = models.DateTimeField(
        auto_now=True,
    )
    
    @property
    def class_title_str(self):
        saved_t = self.class_title
        for value, label in self.CLASS_TITLES_CHOICES:
            if saved_t == value:
                return label

    @property
    def class_status_str(self):
        saved_st = self.class_status
        for value, label in self.CLASS_STATUS_CHOICES:
            if saved_st == value:
                return label
    
    @property
    def class_level_str(self):
        saved_st = self.class_level
        for value, label in self.CLASS_LEVEL_CHOICES:
            if saved_st == value:
                return label
            
    @property
    def class_student_count(self):
        return f"{self.student_profiles.all().count()} of {self.class_capacity}"
    
    @property
    def class_students(self):
        return self.student_profiles.all()
    
    @property
    def class_percent_capacity(self):
        students = self.student_profiles.all().count()
        return f"{round((students/self.class_capacity), 3)} %"

    @property
    def class_subjects_count(self):
        return self.subject_profiles.count()
    
    @property
    def class_subjects(self):
        return self.subject_profiles.all()
    
    @property
    def class_subject_teachers_count(self):
        subjects = self.subject_profiles.all()
        teachers = set()
        for subject in subjects:
            if subject.subject_teacher:
                sb_tid = subject.subject_teacher.teacher_id
                teachers.add(sb_tid)
        return len(teachers)
    
    @property
    def class_full_str(self):
        return f"{self.class_level_str} {self.class_title_str}"
    
    @property
    def class_subject_t_dict(self):
        subject_t_dict = {}
        for subject in self.subject_profiles.all():
            if subject.subject_teacher:
                if subject_t_dict.get(subject.subject_teacher):
                    subject_t_dict[subject.subject_teacher].append(subject.subject_name)
                else:
                    subject_t_dict.update({subject.subject_teacher : [subject.subject_name]})
        return subject_t_dict

    #results processing
    def class_reports_total_generator(self,examination):
        required_reports = self.stereport_profiles.filter(
            streport_examination=examination
        ).order_by("streport_t_score")
        required_results = self.result_profiles.filter(
            result_examination=examination
        )
        for ereport in required_reports:
            sbt_count = self.class_subjects_count
            points = 0
            total = 0
            report_avg = ""
            student = ereport.streport_student
            student_results = required_results.filter(
                result_student = student
            )
            for subject_rez in student_results:
                total += int(subject_rez.result_score)
                points += int(subject_rez.result_p_level[1])
            if total > (89 * sbt_count):
                report_avg = "EE1"
            elif total > (74 * sbt_count):
                report_avg = "EE2"
            elif total > (57 * sbt_count):
                report_avg = "ME1"
            elif total > (40 * sbt_count):
                report_avg = "ME2"
            elif total > (30 * sbt_count):
                report_avg = "AE1"
            elif total > (20 * sbt_count):
                report_avg = "AE2"
            elif total > (10 * sbt_count):
                report_avg = "BE1"
            elif total >=( 0 * sbt_count):
                report_avg = "BE2"
            
            ereport.streport_t_score = total
            ereport.streport_points_score = points
            ereport.streport_p_level = report_avg
            ereport.save(update_fields=["streport_t_score","streport_points_score", "streport_p_level"])
    
    def class_reports_pos_generator(self,examination):
        required_reports = self.stereport_profiles.filter(
            streport_examination=examination
        ).annotate(
            rank=Window(
                expression=DenseRank(),
                order_by=F('streport_t_score').desc(),
            )
        )
        for report in required_reports:
            report.streport_c_position = report.rank
            report.save(update_fields=['streport_c_position'])

    def __str__(self):
        return f"{self.get_class_title_display()}-{self.class_level} ({self.class_school.school_name})"

