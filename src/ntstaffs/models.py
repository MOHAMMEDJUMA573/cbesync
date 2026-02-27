from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser
from schools.models import SchoolProfile
import uuid
from pathlib import Path
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from datetime import date
from dateutil.relativedelta import relativedelta


def generate_unique_ntstaff_id():
    while True:
        new_id = f"NTS-{uuid.uuid4().hex[:16].upper()}"
        if not NtStaffProfile.objects.filter(ntstaff_id=new_id).exists():
            return new_id
        
#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"ntsprf/{fname}{ext}"

class NtStaffProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="ntstaff_profile"
    )

    ntstaff_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_ntstaff_id,
        db_index=True,
        editable=False
    )

    ntstaff_pic = models.ImageField(
        upload_to=image_file_upload_handler,
        null=True,
        blank=True
    )
    ntstaff_school = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name="ntstaffs",
        null=True
    )

    ntstaff_first_name = models.CharField(
        max_length=35
    )
    ntstaff_middle_name = models.CharField(
        max_length=35,
        blank=True,
        null=True
    )
    ntstaff_last_name = models.CharField(
        max_length=35
    )

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    ntstaff_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M'
    )
    ntstaff_dob = models.DateField(
        default=date(2000, 1, 1)
    )
    
    ntstaff_phone = PhoneNumberField(
        help_text="emergency contact"
    )
    ntstaff_email = models.EmailField(
        max_length=100,
        null=True,
        blank=True
    )
    ntstaff_home_address = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="ntstaff address of residence"
    )
    ntstaff_e_contact = PhoneNumberField(
        blank=True,
        help_text="emergency contact"
    )

    QUALIFICATIONS = (
        ("UDGR","Bachelors Degree"),
        ("MSTS", "Masters"),
        ("PHDS", "Doctor of Phylosophy"),
        ("DPLM", "Diploma"),
        ("CTFC", "Certificate")
    )
    ntstaff_h_qualification = models.CharField(
        choices=QUALIFICATIONS,
        max_length=4,
        default="UDGR",
        help_text="Highest ntstaff degree"
    )
    NT_STUDY_FIELD = (
        ("INFT", "Information Tech"),
        ("LAIS", "Lib & Info Science"),
        ("ACAF", "Accounting & Finance"),
        ("MDHS", "Health Services"),
        ("PBAD", "Public Administration"),
        ("OTHS", "Others")
    )
    ntstaff_s_field = models.CharField(
        choices=NT_STUDY_FIELD,
        max_length=4,
        help_text="Study field of the worker"
    )
    ntstaff_y_experience = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(70), MinValueValidator(0)],
        help_text="workers experience in years"
    )
    JOB_TITLE = (
        ('SLBT', 'Lab Technician'),
        ('SSCR', 'Secretary'),
        ('SBSR', 'Bursar'),
        ('SGOF', 'Guidance Officer'),
        ('SNSR', 'School Nurse'),
        ('SSOF', 'Security Officer'), 
        ('SOJT', 'Other'),
    )
    ntstaff_j_title = models.CharField(
        max_length=4,
        choices=JOB_TITLE,
        help_text="The title of the teacher in the school"
    )

    ntstaff_e_notes = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    ALLERGY_CHOICES = (
        ("ENV","Environment"),
        ("FOD","Food"),
        ("LTX", "Latex"),
        ("IST", "Insects")
    )
    ntstaff_allergies = ArrayField(
        models.CharField(max_length=3, choices=ALLERGY_CHOICES),
        blank=True,
        default=list
    )

    STATUS_CHOICES = [
        ('E', 'Employed'),
        ('U', 'Unemployed'),
        ('T', 'Transferred'),
        ('R', 'Reported'),
        ('S', 'Suspended'),
    ]
    ntstaff_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='E'
    )

    ntstaff_creation_date = models.DateTimeField(
        auto_now_add=True
    )
    ntstaff_update = models.DateTimeField(
        auto_now=True
    )

    @property
    def ntstaff_age(self):
        today = date.today()
        dob = self.ntstaff_dob
        age = relativedelta(today, dob)
        years = age.years

        return years
    
    @property
    def ntstaff_title(self):
        saved_t = self.ntstaff_j_title
        for value, label in self.JOB_TITLE:
            if saved_t == value:
                return label


    def __str__(self):
        return f"{self.ntstaff_first_name} {self.ntstaff_last_name} ({self.ntstaff_id})"

    