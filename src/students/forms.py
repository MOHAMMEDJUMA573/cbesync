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
#from django.contrib.postgres.forms import SimpleArrayField

def generate_unique_student_id():
    while True:
        new_id = f"STD-{uuid.uuid4().hex[:16].upper()}"
        if not StudentProfile.objects.filter(student_id=new_id).exists():
            return new_id



class StudentRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        classes_tuple_choices = kwargs.pop("classes_tuple_list")
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["student_class"].choices = classes_tuple_choices

    student_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    student_middle_name = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    student_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    
    student_gender = forms.ChoiceField(
        choices=StudentProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    student_dob = forms.DateField(
        initial=date(2010, 1, 1).strftime('%Y-%m-%d'),
        required=True
    )
    
    student_e_contact = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off"
            }
        ),
        initial="+254",
        label="Mobile No"
    )
    student_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off"
                }
        ),
        max_length=100,
        required=False
    )
    student_home_address = forms.CharField(
        max_length=35,
        required=True
    )
    student_assessment_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        ),
        max_length=35,
        initial="",
        required=False
    )
    student_class = forms.ChoiceField(
    )

    student_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
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
            cleaned_data["student_email"] = r_email.lower()
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

            #increment the nuber of students in the school
            student_school.school_students_polpulation = F(
                'school_students_polpulation'
            ) + 1
            student_school.save(update_fields=['school_students_polpulation'])
         
class StudentSearchForm(forms.Form):
    student_data = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete":"off",
                "placeholder":"Name or SID"
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
    student_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    student_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )

    student_gender = forms.ChoiceField(
        choices=StudentProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    student_id = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    student_class = forms.ChoiceField(

    )
    student_s_needs= forms.ChoiceField(
        choices=StudentProfile.SP_NEEDS_OPTS,
    )


    def clean(self):
        check_flag1 = False
        cleaned_data = super().clean()
        student_fields = [
            "student_first_name", "student_last_name", "student_id",
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
        if not check_flag1:
            nn_fields = [
                "student_gender","student_s_needs"#, "student_class"
            ]
            #for some future validations

        return cleaned_data
     

