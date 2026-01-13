from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from accounts.models import CustomUser

#function to generate random school id
def generate_unique_school_id():
    while True:
        new_id = f"SCH-{uuid.uuid4().hex[:12].upper()}"
        if not School.objects.filter(school_id=new_id).exists():
            return new_id


# Create your models here.
# ======================================
# 1. School Model
# ======================================
class School(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school_id = models.CharField(default=generate_unique_school_id, unique=True, db_index=True, editable=False)
    school_code = models.CharField(max_length=20, unique=True, help_text="Official MOE school code.")
    school_name = models.CharField(max_length=150, help_text="Official school name.")
    #category
    SCHOOL_TYPES_CHOICES = [ ('Day', 'Day'), ('Boarding', 'Boarding'), ('Hybrid', 'Hybrid'), ('Other', 'Other')]
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES_CHOICES, help_text="Type of school i.e Day school")
    # 5. Ownership (enum)
    OWNERSHIP_CHOICES = [('Government', 'Government'), ('Private', 'Private'), ('Community', 'Community'), ('Mission', 'Mission'), ('International', 'International')]
    school_ownership = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES, help_text="School ownership i.e Mission, Private")
    #7.Location fields
    school_county = models.CharField(max_length=50,default='Multi', help_text="County where the school is located.")
    school_subcounty = models.CharField(max_length=50, null=True, help_text="Sub-county for finer location granularity.")
    school_ward = models.CharField(max_length=50, blank=True, null=True, help_text="Optional ward fill for zonal exams management")
    school_location = models.CharField(max_length=255,null=True, help_text="Location of school.")
    #8. Contact fields
    school_email = models.EmailField(max_length=100, help_text="Official school email")
    school_phone = models.CharField(max_length=20, help_text="Official  School tell NO.")
    #9. School status in the site
    STATUS_CHOICES = [ ('Pending', 'Pending Validation'), ('Active', 'Verified'), ('Suspended', 'Suspended')]
    school_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', help_text="School_status on the platform e.g Verified")
    #12. Timestamps
    school_creation_date = models.DateTimeField(auto_now_add=True, help_text="Creation date/time stamp")
    school_updated_date = models.DateTimeField(auto_now=True, help_text="Last Modification timestamp")
    def __str__(self):
        return f"{self.school_name} {self.school_email}"