from django import forms
from datetime import date
from .models import StudentProfile
from accounts.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.postgres.forms import SimpleArrayField

class StudentRegistrationForm(forms.Form):
    student_first_name = forms.CharField(
        max_length=30,
        required=True,
        initial=""
    )
    student_middle_name = forms.CharField(
        max_length=30,
        required=True,
        initial=""
    )
    student_last_name = forms.CharField(
        max_length=30,
        required=True,
        initial=""
    )
    student_gender = forms.ChoiceField(
        choices=StudentProfile.GENDER_CHOICES,
    )
    student_dob = forms.DateField(
        initial=date(2006, 6, 9),
        required=True
    )
    student_e_contact = PhoneNumberField(
        required=True,
        region="KE",
        label="Mobile No"
    )
    student_email = forms.EmailField(
        max_length=30,
        required=False
    )
    student_home_address = forms.CharField(
        max_length=50,
        required=True
    )
    student_admission_number = forms.CharField(
        max_length=20,
        initial="",
        required=True
    )
    #class

    student_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
        disabled=True,
    )
    student_admission_date = forms.DateField(
        initial=date.today(),
        required=True
    )
    student_s_needs= forms.ChoiceField(
        choices=StudentProfile.SP_NEEDS_OPTS,
        required=True
    )
    student_blood_group = forms.ChoiceField(
        choices=StudentProfile.BLOOD_GROUPS,
        required=True
    ) 
    student_e_notes = forms.CharField(
        max_length=200,
        required=False
    )
    student_allergies = SimpleArrayField(
        forms.CharField(max_length=100),
        required=False        
    )
    student_pic = forms.ImageField(
        required=False,
    )






