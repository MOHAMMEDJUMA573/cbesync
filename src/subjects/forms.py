from django import forms
from django.db import transaction
from .models import SubjectProfile
from better_profanity import profanity
from teachers.models import TeacherProfile
from django.utils.translation import gettext_lazy as _



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