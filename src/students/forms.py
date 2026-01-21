from django import forms
from datetime import date
from django.db import transaction
from django.db.models import F
from .models import StudentProfile
from accounts.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
import uuid
from django.utils.translation import gettext_lazy as _
from better_profanity import profanity
#from django.contrib.postgres.forms import SimpleArrayField

def generate_unique_student_id():
    while True:
        new_id = f"STD-{uuid.uuid4().hex[:16].upper()}"
        if not StudentProfile.objects.filter(student_id=new_id).exists():
            return new_id



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
        widget=forms.RadioSelect
    )
    student_dob = forms.DateField(
        initial=date(2006, 6, 9).strftime('%Y-%m-%d'),
        required=True
    )
    student_e_contact = PhoneNumberField(
        required=True,
        initial="+254",
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
        initial=date.today().strftime('%Y-%m-%d'),
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
    student_allergies = forms.MultipleChoiceField(
        choices=StudentProfile.ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    student_pic = forms.ImageField(
    )

    def clean(self):
        cleaned_data =  super().clean()
        student_fields = [
            "student_first_name", "student_middle_name", "student_last_name",
            "student_email"
        ]
        for student_field in student_fields:
            value = cleaned_data.get(student_field).lower()
            if profanity.contains_profanity(value):
                self.add_error(
                    student_field,
                    _(f"{value} is unallowed!")
                )



        return cleaned_data

    def save(self, student_school, commit=True):
        with transaction.atomic():
            username = generate_unique_student_id()
            user = CustomUser.objects.create_user(
                username=username,
                email=self.cleaned_data['student_email'],
                password=str(username),
                user_type='student',
                user_country = self.cleaned_data['student_country'],
            )
            #create the student
            StudentProfile.objects.create(
                user = user,
                student_id = username,
                student_school = student_school,
                student_first_name = self.cleaned_data['student_first_name'],
                student_middle_name = self.cleaned_data['student_middle_name'],
                student_last_name = self.cleaned_data['student_last_name'],
                student_gender = self.cleaned_data['student_gender'],
                student_dob = self.cleaned_data['student_dob'],
                student_e_contact = self.cleaned_data['student_e_contact'],
                student_email = self.cleaned_data['student_email'],
                student_home_address = self.cleaned_data['student_home_address'],
                student_admission_number = self.cleaned_data['student_admission_number'],
                student_admission_date = self.cleaned_data['student_admission_date'],
                student_s_needs = self.cleaned_data['student_s_needs'],
                student_blood_group = self.cleaned_data['student_blood_group'],
                student_e_notes = self.cleaned_data['student_e_notes'],
                student_allergies = self.cleaned_data['student_allergies'],
                student_pic = self.cleaned_data['student_pic'],
                student_status = 'A' #student status default field
            )
            #increment the nuber of students in the school
            student_school.school_students_polpulation = F(
                'school_students_polpulation'
            ) + 1
            student_school.save(update_fields=['school_students_polpulation'])
            print(self.cleaned_data)

