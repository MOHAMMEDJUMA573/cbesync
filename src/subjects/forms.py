from django import forms
from django.db import transaction
from .models import SubjectProfile
from better_profanity import profanity
from teachers.models import TeacherProfile
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import Select

INPUTCSS = "flex flex-1 outline-0 p-2 rounded-md max-w-auto md:max-w-[30ch] bg-inputbg text-inputtxt"

class SubjectCreationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        subject_teachers_choices = kwargs.pop("teachers_tuple_list")
        super(SubjectCreationForm, self).__init__(*args, **kwargs)
        self.fields["subject_teacher"].choices = subject_teachers_choices
    subject_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    subject_class = forms.ChoiceField(
        choices=()
    )
    subject_teacher = forms.ChoiceField(
        choices=()
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        subject_fields = [
            "subject_name"
        ]
        for subject_field in subject_fields:
            value = cleaned_data.get(subject_field)
            if value:
                if profanity.contains_profanity(value):
                    self.add_error(
                        subject_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        #check for none fields
        if not check_flag1:
            nn_fields = [
                "subject_class", "subject_school"
            ]
            #for some future validations
        
        subject_teacher = cleaned_data.get('subject_teacher')
        if not subject_teacher:
            return cleaned_data
        cleaned_data['subject_teacher'] = TeacherProfile.objects.get(
            teacher_id = self.cleaned_data['subject_teacher']
        )


        return cleaned_data
    
    def save(self, subject_school, commit=True):
        with transaction.atomic():
            SubjectProfile.objects.create(
                subject_name = self.cleaned_data['subject_name'],
                subject_school = subject_school,
                subject_class = self.cleaned_data['subject_class'],
                subject_teacher = self.cleaned_data['subject_teacher'],
                subject_status = 'A' #student status default field
            )


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
