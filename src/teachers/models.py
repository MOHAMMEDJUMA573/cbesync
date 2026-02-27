from django.db import models
from  pathlib import Path
from phonenumber_field.modelfields import PhoneNumberField
from schools.models import SchoolProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from datetime import  date
from django.utils import timezone
from accounts.models import CustomUser
import uuid

#funtion to generate random but different teacher ids
def generate_unique_teacher_id():
    while True:
        new_id = f"STD-{uuid.uuid4().hex[:16].upper()}"
        if not TeacherProfile.objects.filter(teacher_id=new_id).exists():
            return new_id
        
#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"tcprf/{fname}{ext}"

# Create your models here.
# ======================================
# 1. Teacher Model
# ======================================
class TeacherProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    
    teacher_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_teacher_id,
        db_index=True,
        editable=False
    )
    teacher_pic = models.ImageField(
        upload_to=image_file_upload_handler,
        null=True,
        help_text="teachers profile pic"
    )
    teacher_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="teacher_profiles",
        null=True
    )
    teacher_tsc_number = models.CharField(
        max_length=35,
        null=True, 
        blank=True, 
        help_text="Teacher's tsc assigned number"
    )


    teacher_first_name = models.CharField(
        max_length=35
    )
    teacher_middle_name = models.CharField(
        max_length=35,
        default=""
    )
    teacher_last_name = models.CharField(
        max_length=35
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    teacher_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
    
    teacher_email = models.EmailField(
        max_length=100,
        null=True
    )
    teacher_phone = PhoneNumberField(
        help_text="contact"
    )
    teacher_e_contact = PhoneNumberField(
        blank=True,
        help_text="teachers emergency contact"
    )
    
    teacher_home_address = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="teacher's address of residence"
    )

    teacher_y_experience = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(70), MinValueValidator(0)],
        help_text="teachers experience in years"
    )
    teacher_h_date = models.DateField(
        help_text="teacher date of hire"
    )
    TEACHER_ROLES = (
        ('PR', 'Principal'),
        ('CT', 'Teacher'),
        ('O', 'Other'),
    )
    teacher_role = models.CharField(
        max_length=2,
        choices=TEACHER_ROLES,
        help_text="The title of the teacher in the school"
    )
    STATUS_CHOICES = (
        ('E', 'Employed  ✅'),
        ('S', 'Suspended  🚟'),
        ('T', 'Transferred 🚅'),
        ('R', 'Retired 🛞'),
    )
    teacher_status = models.CharField(
        max_length=1, 
        choices=STATUS_CHOICES, 
        default='E', 
        help_text="Teachers employment status"
    )
    TEACHER_EMPLOYERS = (
        ("GOVT", "Government"),
        ("INST", "Institution"),
        ("TPPR", "T Practice"),
        ("OTHR", "Other")
    )
    teacher_employer = models.CharField(
        choices=TEACHER_EMPLOYERS,
        max_length=4,
        default="INST"
    )
    TEACHER_DEPARTMENTS = (
        ("STDP", "Science & Technology"),
        ("PSDP", "Science Department"),
        ("HMDP", "Humanities Dept. "),
        ("CAPE", "C.A & Physical Ed. "),
        ("MTDP", "Mathematics Department")
    )
    teacher_department = models.CharField(
        choices=TEACHER_DEPARTMENTS,
        max_length=4,
        help_text="Dept the teacher belongs to"
    )
    EDUCATION_LEVELS = (
        ("PPR", "Pre-Primary"),
        ("LPR", "Low-Primary"),
        ("UPR", "Upper-Primary"),
        ("JSS", "Junior-Secondary"),
    )
    teacher_e_level = models.CharField(
        choices=EDUCATION_LEVELS,
        max_length=3,
        help_text="Level the teacher teaches"
    )
    TEACHING_SUBJECTS = (
        ("ENGL", "English"),
        ("KISW", "Kiswahili"),
        ("MATS", "Maths"),
        ("RESD", "R.Edu."),
        ("ISCE", "I. Science"),
        ("SSTD", "S.Studies"),
        ("ANTR", "A.&Nutri"),
        ("CASP", "C&Sports"),
        ("PRTS", "Pre-Tech")
    )
    teacher_t_subjects = ArrayField(
        models.CharField(max_length=4, choices=TEACHING_SUBJECTS),
        blank=True,
        default=list
    )
    QUALIFICATIONS = (
        ("UDGR","Bachelor's Degree"),
        ("MSTS", "Masters"),
        ("PHDS", "Doctor of Phylosophy"),
        ("DPLM", "Diploma"),
        ("CTFC", "Certificate")
    )
    teacher_h_qualification = models.CharField(
        choices=QUALIFICATIONS,
        max_length=4,
        default="UDGR",
        help_text="Highest teacher degree"
    )

    teacher_creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Simply the day the teacher was added into the system"
    )
    teacher_updated_date = models.DateTimeField(
        auto_now=True, help_text="Last time the record was updated"
    )
    
    @property
    def teacher_full_name(self):
        return f"{self.teacher_first_name} {self.teacher_last_name[:4]}... {self.teacher_id[:8]}..."
    
    @property
    def teacher_h_qualification_str(self):
        saved_hq = self.teacher_h_qualification
        for value, label in self.QUALIFICATIONS:
            if saved_hq == value:
                return label

    @property
    def teacher_role_str(self):
        saved_role = self.teacher_role
        for value, label in self.TEACHER_ROLES:
            if saved_role == value:
                return label

    @property
    def teacher_teaching_subjects(self):
        return self.subject_profiles.all()
    
    @property
    def teacher_ct_classes(self):
        return self.classt_profiles.all()
    def __str__(self):
        return f"{self.teacher_first_name} {self.teacher_last_name} {self.teacher_tsc_number}"