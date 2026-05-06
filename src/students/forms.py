from django import forms
from datetime import date
from django.db import transaction
from django.db.models import F
from .models import StudentProfile
from classes.models import ClassProfile
from accounts.models import CustomUser
from results.models import ResultsProfile
from reports.models import StudentEReportProfile
from phonenumber_field.formfields import PhoneNumberField
import uuid
from django.utils.translation import gettext_lazy as _
from better_profanity import profanity
from django.forms.widgets import Select, FileInput
#from django.contrib.postgres.forms import SimpleArrayField

def generate_unique_student_id():
    while True:
        new_id = f"STD-{uuid.uuid4().hex[:16].upper()}"
        if not StudentProfile.objects.filter(student_id=new_id).exists():
            return new_id

INPUTCSS = "flex flex-1 outline-0 p-2 rounded-md max-w-auto md:max-w-[30ch] bg-inputbg text-inputtxt border border-bordercl"

class StudentRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        classes_tuple_choices = kwargs.pop("classes_tuple_list")
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["student_class"].choices = classes_tuple_choices

    student_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    student_middle_name = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    student_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    
    student_gender = forms.ChoiceField(
        choices=StudentProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    student_dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class":INPUTCSS,
                "type":"date"
            }
        ),
        initial=date(2010, 1, 1).strftime('%Y-%m-%d'),
        required=True
    )
    
    student_e_contact = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off",
                "class":INPUTCSS
            }
        ),
        initial="+254",
        label="Mobile No"
    )
    student_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off",
                "class":INPUTCSS
            }
        ),
        max_length=100,
        required=False
    )
    student_home_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":INPUTCSS
            }
        ),
        max_length=35,
        required=True
    )
    student_assessment_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        ),
        max_length=35,
        initial="",
        required=False
    )
    student_class = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        )
    )

    student_country = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
    )
    student_admission_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class":INPUTCSS
            }
        ),
        initial=date.today().strftime('%Y-%m-%d'),
        required=True
    )
    student_s_needs= forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=StudentProfile.SP_NEEDS_OPTS,
        required=True
    )
    student_blood_group = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=StudentProfile.BLOOD_GROUPS,
        required=True
    ) 
    student_e_notes = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows":3,
                "cols":5,
                "class":INPUTCSS
            }
        )
    )
    student_allergies = forms.MultipleChoiceField(
        choices=StudentProfile.ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    student_pic = forms.ImageField(
        widget=FileInput(
            attrs={
                "class":INPUTCSS
            }
        ),
        required=False
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        student_fields = [
            "student_first_name", "student_middle_name", "student_last_name",
            "student_email"
        ]
        for student_field in student_fields:
            value = cleaned_data.get(student_field)
            if value:
                if profanity.contains_profanity(value):
                    self.add_error(
                        student_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        if check_flag1:
            return cleaned_data
        #check for none fields
        student_middle_name = cleaned_data.get('student_middle_name')
        if not student_middle_name:
            cleaned_data['student_middle_name'] = ""
        r_email = cleaned_data.get("student_email")
        if r_email:
            email = r_email.lower()
            cleaned_data["student_email"] = email
            if CustomUser.objects.filter(email__iexact=email).exists():
                self.add_error(
                    "student_email",
                    _("Email already in use!")
                )
        #validate date of birth later on
        #get the keyed fields
        student_classes = cleaned_data.get('student_class')
        if not student_classes:
            return cleaned_data
        try:
            cleaned_data['student_class'] = ClassProfile.objects.get(
                class_id = self.cleaned_data['student_class']
            )
        except ClassProfile.DoesNotExist:
            self.add_error(
                "student_class",
                _("The class does not exist")
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
            student_saved = StudentProfile.objects.create(
                user = user,
                student_id = username,
                student_school = student_school,
                student_class = self.cleaned_data['student_class'],
                student_first_name = (self.cleaned_data['student_first_name']).title(),
                student_middle_name = (self.cleaned_data['student_middle_name']).title(),
                student_last_name = (self.cleaned_data['student_last_name']).title(),
                student_gender = self.cleaned_data['student_gender'],
                student_dob = self.cleaned_data['student_dob'],
                student_e_contact = self.cleaned_data['student_e_contact'],
                student_email = self.cleaned_data['student_email'],
                student_home_address = self.cleaned_data['student_home_address'],
                student_assessment_number = self.cleaned_data['student_assessment_number'],
                student_admission_date = self.cleaned_data['student_admission_date'],
                student_s_needs = self.cleaned_data['student_s_needs'],
                student_blood_group = self.cleaned_data['student_blood_group'],
                student_e_notes = self.cleaned_data['student_e_notes'],
                student_allergies = self.cleaned_data['student_allergies'],
                student_pic = self.cleaned_data['student_pic'],
                student_status = 'A' #student status default field
            )
            #create results for the student
            student_class = self.cleaned_data['student_class']
            student_class_examinations = student_class.examination_profiles.all()
            student_class_subjects = student_class.subject_profiles.all()
            for examination in student_class_examinations:
                for subject in student_class_subjects:
                    ResultsProfile.objects.create(
                        result_student = student_saved,
                        result_class = student_class,
                        result_school = student_class.class_school,
                        result_subject = subject,
                        result_examination = examination
                    )
                StudentEReportProfile.objects.create(
                    streport_examination = examination,
                    streport_class = student_class,
                    streport_student = student_saved,
                )
         
class StudentSearchForm(forms.Form):
    student_data = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete":"off",
                "placeholder":"Name or SID",
                "class":"flex flex-1 outline-0 rounded-md max-w-auto md:max-w-[30ch] ml-4 mr-4 text-inputtxt"
            }
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        search_data = cleaned_data.get("student_data")
        if search_data:
            if profanity.contains_profanity(search_data.lower()):
                    self.add_error(
                        "student_data",
                        _(f"{profanity.censor(search_data)} is unallowed!")
                    )
        else:
            self.add_error(
                "student_data",
                _(f"Empty")
            )


        return cleaned_data

class StudentEnrollmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        classes_tuple_choices = kwargs.pop("classes_tuple_list")
        super(StudentEnrollmentForm, self).__init__(*args, **kwargs)
        self.fields["student_class"].choices = classes_tuple_choices

    student_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    student_middle_name = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    student_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    student_id = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    student_class = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )
    student_dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class":INPUTCSS,
                "type": "date"
            }
        ),
        initial=date(2010, 1, 1).strftime('%Y-%m-%d'),
        required=True
    )


    def clean(self):
        check_flag1 = False
        cleaned_data = super().clean()
        student_fields = [
            "student_first_name","student_middle_name","student_last_name"
        ]
        for student_field in student_fields:
            value = cleaned_data.get(student_field)
            if value:
                value = value.title()
                cleaned_data[student_field] = value
                if profanity.contains_profanity(value):
                    self.add_error(
                        student_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        if check_flag1:
            return cleaned_data
        
        #for some future validations
        #get the keyed fields
        student_classid = cleaned_data.get('student_class')
        if not student_classid:
            return cleaned_data
        try:
            cleaned_data['student_class'] = ClassProfile.objects.get(
                class_id = student_classid
            )
        except ClassProfile.DoesNotExist:
            self.add_error(
                "student_class",
                _("The class does not exist")
            )

        return cleaned_data
     

