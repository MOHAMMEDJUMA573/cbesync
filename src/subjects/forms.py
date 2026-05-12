from django import forms
from django.db import transaction
from .models import SubjectProfile
from better_profanity import profanity
from teachers.models import TeacherProfile
from classes.models import ClassProfile
from results.models import ResultsProfile
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import Select

INPUTCSS = "flex flex-1 outline-0 p-2 rounded-md max-w-auto md:max-w-[30ch] bg-inputbg text-inputtxt border border-bordercl"

class SubjectCreationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        subject_teachers_choices = kwargs.pop("teachers_tuple_list")
        subject_classes_choices = kwargs.pop("classes_tuple_list")
        super(SubjectCreationForm, self).__init__(*args, **kwargs)
        self.fields["subject_teacher"].choices = subject_teachers_choices
        self.fields["subject_class"].choices = subject_classes_choices
    subject_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                'class':INPUTCSS
            }
        )
    )
    subject_code = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                'class':INPUTCSS
            }
        )
    )
    subject_class = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )
    subject_teacher = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        subject_fields = [
            "subject_name","subject_code"
        ]
        for subject_field in subject_fields:
            value = cleaned_data.get(subject_field)
            if value:
                if subject_field == "subject_code":
                    value = value.upper()
                else:
                    value = value.title()
                cleaned_data[subject_field] = value
                if profanity.contains_profanity(value):
                    self.add_error(
                        subject_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        #check for none fields 
        if not check_flag1:       
            subject_class = cleaned_data.get('subject_class')
            subject_teacher = cleaned_data.get('subject_teacher')
            if  subject_class and subject_teacher:
                cleaned_data['subject_class'] = ClassProfile.objects.get(
                    class_id = subject_class
                )
                cleaned_data['subject_teacher'] = TeacherProfile.objects.get(
                    teacher_id = subject_teacher
                )
                #make sure subject are below 9
                c_subject_count = cleaned_data["subject_class"].class_subjects_count
                if c_subject_count >= 9:
                    raise forms.ValidationError("Class has max number of subjects (9)")
            else:
                return cleaned_data

        return cleaned_data
    
    def save(self, commit=True):
        subject_class = self.cleaned_data['subject_class']
        subject_school = subject_class.class_school
        subject_program = subject_class.class_program        
        with transaction.atomic():
            created_subject = SubjectProfile.objects.create(
                subject_name =self.cleaned_data['subject_name'],
                subject_code = self.cleaned_data['subject_code'],
                subject_school = subject_school,
                subject_class = subject_class,
                subject_program = subject_program,
                subject_teacher =self.cleaned_data['subject_teacher'],
            )
            #get all students and add results for them
            subject_students = subject_class.class_students
            subject_examinations = subject_class.examination_profiles.all()
            for examination in subject_examinations:
                for student in subject_students:
                    ResultsProfile.objects.create(
                        result_student = student,
                        result_class = subject_class,
                        result_school = subject_class.class_school,
                        result_subject = created_subject,
                        result_examination = examination
                    )
                    
            return created_subject

class SubjectDeletionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        subject_classes_choices = kwargs.pop("classes_tuple")
        school_subjects_choices = kwargs.pop("subjects_tuple")
        super(SubjectDeletionForm, self).__init__(*args, **kwargs)
        self.fields["subject_class"].choices = subject_classes_choices
        self.fields["subject_id"].choices = school_subjects_choices
    subject_code = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                'class':INPUTCSS
            }
        )
    )
    subject_id = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )
    subject_class = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        subject_fields = [
            "subject_code"
        ]
        for subject_field in subject_fields:
            value = cleaned_data.get(subject_field)
            if value:
                if subject_field == "subject_code":
                    value = value.upper()
                else:
                    value = value.title()
                cleaned_data[subject_field] = value
                if profanity.contains_profanity(value):
                    self.add_error(
                        subject_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        #check for none fields 
        if not check_flag1:
            if cleaned_data.get("subject_id") and cleaned_data.get("subject_class") and cleaned_data.get("subject_code"):
                subject = SubjectProfile.objects.get(
                    subject_id=cleaned_data["subject_id"]
                )
                subject_class = ClassProfile.objects.get(
                    class_id=cleaned_data["subject_class"]
                )
                cleaned_data["subject_id"] = subject
                cleaned_data["subject_class"] = subject_class
                class_subjects = subject_class.class_subjects
                if subject in class_subjects:
                    subject_code = subject.subject_code
                    passed_s_code = cleaned_data["subject_code"]
                    if subject_code != passed_s_code:
                        raise forms.ValidationError(
                            _("Wrong subject code + subject combination!")
                        )
                else:
                    raise forms.ValidationError(
                        _("Wrong subject + class combination!")
                    )
            
        return cleaned_data



class SubjectTeacherAllocationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        subjects_tuple_choices = kwargs.pop("subjects_tuple_list")
        teachers_tuple_choices = kwargs.pop("teachers_tuple_list")
        super(SubjectTeacherAllocationForm, self).__init__(*args, **kwargs)
        self.fields["subjects_objs"].choices = subjects_tuple_choices
        self.fields["teachers_objs"].choices = teachers_tuple_choices

    subjects_objs = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )
    teachers_objs = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=()
    )

    def clean(self):
        cleaned_data = super().clean()
        subject_passed = cleaned_data.get("subjects_objs")
        teacher_passed = cleaned_data.get("teachers_objs")
        if subject_passed and teacher_passed:
            try:
                subject_obj = SubjectProfile.objects.get(subject_id=subject_passed)
                teacher_obj = TeacherProfile.objects.get(teacher_id=teacher_passed)
                cleaned_data["subjects_objs"] = subject_obj
                cleaned_data["teacher_objs"] = teacher_obj
            except (SubjectProfile.DoesNotExist, TeacherProfile.DoesNotExist):
                raise forms.ValidationError("Non existent options ")
        return cleaned_data
            
    def save(self):
        with transaction.atomic():
            subject_passed = self.cleaned_data["subjects_objs"]
            subject_passed.subject_teacher = self.cleaned_data["teacher_objs"]
            subject_passed.save(update_fields=["subject_teacher"])
