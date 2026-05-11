from django import forms
from datetime import date
from django.db import transaction
from django.db.models import F
from .models import TeacherProfile
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumber
import uuid
from django.utils.translation import gettext_lazy as _
from better_profanity import profanity
from django.forms.widgets import Select, ClearableFileInput

#funtion to generate random but different teacher ids
def generate_unique_teacher_id():
    while True:
        new_id = f"TCH-{uuid.uuid4().hex[:12].upper()}"
        if not TeacherProfile.objects.filter(teacher_id=new_id).exists():
            return new_id

INPUTCSS = "flex flex-1 outline-0 p-2 rounded-md max-w-auto md:max-w-[30ch] bg-inputbg text-inputtxt border border-bordercl"

class TeacherRegistrationForm(forms.Form):
    teacher_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class": INPUTCSS
            }
        )
    )
    teacher_middle_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class": INPUTCSS
            }
        )
    )
    teacher_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class": INPUTCSS
            }
        )
    )

    teacher_gender = forms.ChoiceField(
        choices=TeacherProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    
    teacher_phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off",
                "class": INPUTCSS
            }
        ),
        initial="+254",
        label="Mobile No",
    )
    teacher_e_contact = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off",
                "class": INPUTCSS
            }
        ),
        initial="+254",
        label="Mobile No"
    )
    
    teacher_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off",
                "class": INPUTCSS
            }
        ),
        max_length=100,
    )
    teacher_home_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": INPUTCSS
            }
        ),
        max_length=50,
    )
    teacher_y_experience = forms.IntegerField(
        initial=0,
        widget=forms.NumberInput(
            attrs={
                "max":70,
                "min":0,
                "class": INPUTCSS
            }
        ),
        help_text="teachers experience"
    )
    teacher_h_date = forms.DateField(
        initial=date.today().strftime('%Y-%m-%d'),
        widget=forms.DateInput(
            attrs={
                "class": INPUTCSS,
                "type":"date"
            }
        )
    )
    teacher_country = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
    )
    teacher_employer = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.TEACHER_EMPLOYERS,
        initial="GOVT",
    )
    teacher_department = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.TEACHER_DEPARTMENTS,
        initial="STPD",
    )
    teacher_role = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.TEACHER_ROLES,
        initial="CT",
    )
    teacher_h_qualification = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.QUALIFICATIONS,
        initial="UDGR"
    )
    teacher_pic = forms.ImageField(
        widget=ClearableFileInput(
            attrs={
                "class": INPUTCSS
            }
        ),
        required=False
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        teacher_fields = [
            "teacher_first_name", "teacher_middle_name", "teacher_last_name",
        ]
        for teacher_field in teacher_fields:
            value = cleaned_data.get(teacher_field)
            if value:
                value = value.title()
                self.cleaned_data[teacher_field] = value
                if profanity.contains_profanity(value):
                    self.add_error(
                        teacher_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        if check_flag1:
            return cleaned_data
            
        r_email = cleaned_data.get("teacher_email")
        if r_email:
            email = r_email.lower()
            cleaned_data["teacher_email"] = email
            if CustomUser.objects.filter(email__iexact=email).exists():
                self.add_error(
                    "teacher_email",
                    _("Email already in use!")
                )
        #reasonable exp
        xp = cleaned_data.get("teacher_y_experience")
        if xp and (xp > 70 or xp < 0) :
            self.add_error(
                "teacher_y_experience",
                _("> 0 and <70 ? ")
            )

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
            #create the teacher
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
                teacher_y_experience = self.cleaned_data['teacher_y_experience'],
                teacher_h_date = self.cleaned_data['teacher_h_date'],
                teacher_employer = self.cleaned_data['teacher_employer'],
                teacher_department = self.cleaned_data['teacher_department'],
                teacher_role = self.cleaned_data['teacher_role'],
                teacher_h_qualification = self.cleaned_data['teacher_h_qualification'],
                teacher_pic = self.cleaned_data['teacher_pic'],
                teacher_status = 'E' 
            )
            
class TeacherSearchForm(forms.Form):
    teacher_data = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete":"off",
                "placeholder":"Name or TID",
                "class":"flex flex-1 outline-0 rounded-md max-w-auto md:max-w-[30ch] ml-4 mr-4 text-inputtxt"
            }
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        search_data = cleaned_data.get("teacher_data")
        if search_data:
            if profanity.contains_profanity(search_data.lower()):
                    self.add_error(
                        "teacher_data",
                        _(f"{profanity.censor(search_data)} is unallowed!")
                    )
        else:
            self.add_error(
                "teacher_data",
                _(f"Empty")
            )

        return cleaned_data

class TeacherEnrollmentForm(forms.Form):
    teacher_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class": INPUTCSS
            }
        )
    )
    teacher_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class": INPUTCSS
            }
        )
    )

    teacher_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off",
                "class": INPUTCSS
            }
        ),
        max_length=100,
        required=False
    )
    teacher_id = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class": INPUTCSS
            }
        )
    )
    
    teacher_phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off",
                "class": INPUTCSS
            }
        ),
        initial="+254",
        label="Mobile No",
    )
    teacher_role = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.TEACHER_ROLES,
        initial="CT",
    )
    teacher_e_level = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.EDUCATION_LEVELS,
        initial="JSS"
    )
    teacher_t_subjects = forms.MultipleChoiceField(
        choices=TeacherProfile.TEACHING_SUBJECTS,
        widget=forms.CheckboxSelectMultiple,
    )
    teacher_h_qualification = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=TeacherProfile.QUALIFICATIONS,
        initial="UDGR"
    )


    def clean(self):
        check_flag1 = False
        cleaned_data = super().clean()
        teacher_fields = [
            "teacher_first_name", "teacher_last_name", "teacher_email"
        ]
        for teacher_field in teacher_fields:
            value = cleaned_data.get(teacher_field)
            if value:
                value = value.title()
                cleaned_data[teacher_field] = value
                if profanity.contains_profanity(value):
                    self.add_error(
                        teacher_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        if check_flag1:
            return cleaned_data

        r_email = cleaned_data.get("teacher_email")
        if r_email:
            email = r_email.lower()
            cleaned_data["teacher_email"] = email
            if CustomUser.objects.filter(email__iexact=email).exists():
                self.add_error(
                    "teacher_email",
                    _("Email already in use!")
                )

        return cleaned_data
     
