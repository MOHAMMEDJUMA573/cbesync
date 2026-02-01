from django.db import models
from datetime import date
from pathlib import Path
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password
import uuid
from accounts.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from dateutil.relativedelta import relativedelta


#function to generate a path
def image_file_upload_handler(instance, filename):
    fname = uuid.uuid4().hex
    ext = Path(filename).suffix
    return f"scprf/{fname}{ext}"

#function to generate random school id
def generate_unique_school_id():
    while True:
        new_id = f"SCH-{uuid.uuid4().hex[:12].upper()}"
        if not SchoolProfile.objects.filter(school_id=new_id).exists():
            return new_id


# Create your models here.
# ======================================
# 1. School Model
# ======================================
class SchoolProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="school_profile"
    )
    school_id = models.CharField(
        default=generate_unique_school_id,
        unique=True,
        db_index=True,
        editable=False
    )
    school_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Official MOE school code."
    )
    school_name = models.CharField(
        max_length=150,
        help_text="Official school name."
    )
    school_badge = models.ImageField(
        upload_to=image_file_upload_handler,
        blank=True,
        null=True
    )
    #category
    SCHOOL_TYPES_CHOICES = [
        ('D', 'Day'),
        ('B', 'Boarding'),
        ('H', 'Hybrid'),
        ('O', 'Other')
    ]
    school_type = models.CharField(
        max_length=20, default='D',
        choices=SCHOOL_TYPES_CHOICES,
        help_text="Type of school i.e Day school"
    )
    # 5. Ownership (enum)
    OWNERSHIP_CHOICES = [
        ('GOVT', 'Government'),
        ('PRVT', 'Private'),
        ('CMTY', 'Community'),
        ('MSSN', 'Mission'),
        ('INTL', 'International')
    ]
    school_ownership = models.CharField(
        max_length=20,default='GOVT',
        choices=OWNERSHIP_CHOICES,
        help_text="School ownership i.e Mission, Private"
    )
    #7.Location fields
    KENYA_PRV_CBESYNC = [
        ("CST", "Coast"),
        ("CEN", "Central"),
        ("EAS", "Eastern"),
        ("NBO", "Nairobi"),
        ("NEA", "North Eastern"),
        ("NYA", "Nyanza"),
        ("RVT", "Rift Valley"),
        ("WES", "Western")
    ]
    school_admin_level_1 = models.CharField(
        max_length=50,
        choices=KENYA_PRV_CBESYNC,
        blank=False,
        default="CST",
        help_text="State / Province / Region"
    )
    KENYA_CNT_CBESYNC = [
        ("EMB", "Embu"),
        ("BNG", "Bungoma"),
        ("BMT", "Bomet"),
        ("BRG", "Baringo"),
        ("BUS", "Busia"),
        ("GRS", "Garissa"),
        ("HBY", "Homa Bay"),
        ("ISL", "Isiolo"),
        ("KJD", "Kajiado"),
        ("KMB", "Kiambu"),
        ("KSI", "Kisii"),
        ("KSM", "Kisumu"),
        ("KKG", "Kakamega"),
        ("KIT", "Kitui"),
        ("KLF", "Kilifi"),
        ("KRC", "Kericho"),
        ("LKP", "Laikipia"),
        ("LMU", "Lamu"),
        ("MSA", "Mombasa"),
        ("MCH", "Machakos"),
        ("MDR", "Mandera"),
        ("MKU", "Makueni"),
        ("MER", "Meru"),
        ("MSB", "Marsabit"),
        ("MGR", "Migori"),
        ("MUG", "Murang'a"),
        ("NKU", "Nakuru"),
        ("NEA", "North Eastern"),
        ("NRK", "Narok"),
        ("NYD", "Nyandarua"),
        ("NYM", "Nyamira"),
        ("NYR", "Nyeri"),
        ("SMB", "Samburu"),
        ("SIA", "Siaya"),
        ("TNR", "Tana River"),
        ("TNZ", "Trans-Nzoia"),
        ("TNT", "Tharaka-Nithi"),
        ("TRK", "Turkana"),
        ("TTV", "Taita-Taveta"),
        ("UAS", "Uasin Gishu"),
        ("VHG", "Vihiga"),
        ("WAJ", "Wajir"),
        ("WPK", "West Pokot"),
        ("NRB", "Nairobi")
    ]

    school_admin_level_2 = models.CharField(
        max_length=50,
        choices=KENYA_CNT_CBESYNC,
        null=False,
        blank=False,
        default="MBS",
        help_text="County / District / Prefecture"
    )
    school_admin_level_3 = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default="Likoni",
        help_text="Ward / Municipality / Commune"
    )
    school_locality = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default="Maweni",
        help_text="Village / Town / Neighborhood"
    )    #8. Contact fields
    school_email = models.EmailField(
        max_length=100,
        unique=True,
        help_text="Official school email"
    )
    school_phone = PhoneNumberField(
        blank=True
    )
    #9. School status in the site
    STATUS_CHOICES = [
        ('P', 'Pending Validation'),
        ('V', 'Verified'),
        ('S', 'Suspended')
    ]
    school_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P',
        help_text="School_status on the platform e.g Verified"
    )
    #school_polpulation
    school_students_polpulation = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5000), MinValueValidator(0)],
        help_text="Number of students"
    )
    school_teachers_polpulation = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(500), MinValueValidator(0)],
        help_text="Number of teachers"
    )
    school_ntstaffs_polpulation = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(500), MinValueValidator(0)],
        help_text="Number of ntstaffs"
    )
    school_parents_polpulation = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(2500), MinValueValidator(0)],
        help_text="Number of ntstaffs"
    )
    #12. Timestamps
    school_creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation date/time stamp",
        editable=False
    )
    school_updated_date = models.DateTimeField(
        auto_now=True,
        help_text="Last Modification timestamp"
    )
    #return string

    @property
    def school_polpulation(self):
        return (self.school_students_polpulation + self.school_teachers_polpulation + self.school_ntstaffs_polpulation)

    @property
    def school_online_days(self):
        today = date.today()
        school_doc = self.school_creation_date.date()
        days_age = relativedelta(today, school_doc).days
        return  days_age

    def __str__(self):
        return f"{self.school_name} --- {self.school_email}"
    
    