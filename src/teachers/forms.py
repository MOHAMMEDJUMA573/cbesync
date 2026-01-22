from django import forms
from datetime import date
from django.db import transaction
from django.db.models import F
from .models import TeacherProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
import uuid
from django.utils.translation import gettext_lazy as _
from better_profanity import profanity

#funtion to generate random but different teacher ids
def generate_unique_teacher_id():
    while True:
        new_id = f"TCH-{uuid.uuid4().hex[:12].upper()}"
        if not TeacherProfile.objects.filter(teacher_id=new_id).exists():
            return new_id

class TeacherRegistrationForm(forms.Form):
    teacher_first_name = forms.CharField(
        max_length=30,
    )
    teacher_middle_name = forms.CharField(
        max_length=30,
    )
    teacher_last_name = forms.CharField(
        max_length=30,
    )

    teacher_gender = forms.ChoiceField(
        choices=TeacherProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    
    teacher_phone = PhoneNumberField(
        initial="+254",
        label="Mobile No"
    )
    teacher_e_contact = PhoneNumberField(
        initial="+254",
        label="Mobile No"
    )
    
    teacher_email = forms.EmailField(
        max_length=30,
    )
    teacher_home_address = forms.CharField(
        max_length=50,
    )

    teacher_tsc_number = forms.CharField(
        max_length=30,
        help_text="Teacher's tsc assigned number"
    )
    teacher_y_experience = forms.IntegerField(
        initial=0,
        # validators=[MaxValueValidator(60), MinValueValidator(0)],
        help_text="teachers experience"
    )
    teacher_h_date = forms.DateField(
        initial=date.today().strftime('%Y-%m-%d'),
    )
    teacher_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
    )
    teacher_employer = forms.ChoiceField(
        choices=TeacherProfile.TEACHER_EMPLOYERS,
        initial="GOVT",
    )
    teacher_department = forms.ChoiceField(
        choices=TeacherProfile.TEACHER_DEPARTMENTS,
        initial="STPD",
    )
    teacher_role = forms.ChoiceField(
        choices=TeacherProfile.TEACHER_ROLES,
        initial="CT",
    )
    teacher_e_level = forms.ChoiceField(
        choices=TeacherProfile.EDUCATION_LEVELS,
        initial="JSS"
    )
    teacher_t_subjects = forms.MultipleChoiceField(
        choices=TeacherProfile.TEACHING_SUBJECTS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    teacher_h_qualification = forms.ChoiceField(
        choices=TeacherProfile.QUALIFICATIONS,
        initial="UDGR"
    )
    teacher_pic = forms.ImageField(
        required=False
    )

    def clean(self):
        cleaned_data =  super().clean()
        return cleaned_data

    def save(self, teacher_school, commit=True):
        with transaction.atomic():
            username = generate_unique_teacher_id()
            user = CustomUser.objects.create_user(
                username=username,
                email=self.cleaned_data['teacher_email'],
                password=str(username),
                user_type='teacher',
                user_country = self.cleaned_data['teacher_country'],
            )
            #create the student
            TeacherProfile.objects.create(
                user = user,
                teacher_id = username,
                teacher_school = teacher_school,
                teacher_first_name = self.cleaned_data['teacher_first_name'],
                teacher_middle_name = self.cleaned_data['teacher_middle_name'],
                teacher_last_name = self.cleaned_data['teacher_last_name'],
                teacher_gender = self.cleaned_data['teacher_gender'],
                teacher_phone = self.cleaned_data['teacher_phone'],
                teacher_e_contact = self.cleaned_data['teacher_e_contact'],
                teacher_email = self.cleaned_data['teacher_email'],
                teacher_home_address = self.cleaned_data['teacher_home_address'],
                teacher_tsc_number = self.cleaned_data['teacher_tsc_number'],
                teacher_y_experience = self.cleaned_data['teacher_y_experience'],
                teacher_h_date = self.cleaned_data['teacher_h_date'],
                teacher_employer = self.cleaned_data['teacher_employer'],
                teacher_department = self.cleaned_data['teacher_department'],
                teacher_role = self.cleaned_data['teacher_role'],
                teacher_t_subjects = self.cleaned_data['teacher_t_subjects'],
                teacher_e_level = self.cleaned_data['teacher_e_level'],
                teacher_h_qualification = self.cleaned_data['teacher_h_qualification'],
                teacher_pic = self.cleaned_data['teacher_pic'],
                teacher_status = 'A' #teacher status default field
            )
            #increment the nuber of students in the school
            teacher_school.school_teachers_polpulation = F(
                'school_teachers_polpulation'
            ) + 1
            teacher_school.save(update_fields=['school_teachers_polpulation'])
            print(self.cleaned_data)
