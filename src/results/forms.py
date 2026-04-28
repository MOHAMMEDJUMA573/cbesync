from django import forms
from django.db import transaction
import uuid
from.models import ResultsProfile
from subjects.models import SubjectProfile
from classes.models import ClassProfile
from students.models import StudentProfile
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.forms.widgets import Select

RESULT_PERIOD_CHOICES = [
    ('Opener', 'Opener'),
    ('Mid', 'Mid-Term'),
    ('End', 'End-Term')
]
RESULT_TERM_CHOICES = [
    ('T 1', 'Term 1'),
    ('T 2', 'Term 2'),
    ('T 3', 'Term 3'),
]
INPUTCSS = "flex flex-1 outline-0 p-2 rounded-md max-w-auto md:max-w-[30ch] bg-inputbg text-inputtxt border border-bordercl"

class ResultsSubmissionForm(forms.ModelForm):
    class Meta:
        model = ResultsProfile
        fields = ["result_score"]
        widgets = {
            "result_score": forms.NumberInput(attrs={"max": 100, "min": 0, "step": "any"}),
        }

    def __init__(self, *args, **kwargs):
        # Pop the teacher so we can use it in save()
        self.results_teacher = kwargs.pop('result_teacher', None)
        super().__init__(*args, **kwargs)
        if 'result_id' in self.fields:           
            self.fields['result_id'].widget = forms.HiddenInput()
    
    def clean_result_score(self):
        score = self.cleaned_data.get("result_score")
        if score is not None:
            if score < 0 or score > 100:
                self.add_error(
                    "result_score",
                    _("Score out of range!")
                )
        return score
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.results_teacher is not None:
            instance.result_teacher = self.results_teacher
        if commit:
            instance.save(update_fields=["result_score", "result_teacher"])
        return instance
            

#school results filter form 
class ResultsFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        classes_tuple_choices = kwargs.pop("classes_tuple_list")
        super(ResultsFilterForm, self).__init__(*args, **kwargs)
        self.fields["result_class"].choices = classes_tuple_choices
    
    result_class = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices = ()
    )
    result_term = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=RESULT_TERM_CHOICES
    )
    result_period = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=RESULT_PERIOD_CHOICES
    )
    current_year = int((datetime.today()).year)
    RESULTS_YEAR_CHOICES = [
        (str(c), c)
        for c in range((current_year-10),(current_year+10),1)
    ]
    result_year = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=RESULTS_YEAR_CHOICES,
        initial=int((datetime.today()).year)
    )
    VIEW_RESULTS_OPTION = [
        (0, "View"),
        (1, "Print")
    ]
    result_options = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": INPUTCSS
            }
        ),
        choices=VIEW_RESULTS_OPTION,
        initial=0
    )   
    
    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        #get the class
        class_passed = cleaned_data.get("result_class")
        if class_passed:
            class_passed = ClassProfile.objects.get(class_id=class_passed)
            cleaned_data["result_class"] = class_passed
                    
        return cleaned_data
    
#teachers page to select the class for which he is to update scores
class TeacherResultsUploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        subjects_tuple_choices = kwargs.pop("subjects_tuple_choices")
        super(TeacherResultsUploadForm, self).__init__(*args, **kwargs)
        self.fields["results_subjects"].choices = subjects_tuple_choices
    results_subjects =forms.ChoiceField(
        choices=()
    )
    results_terms = forms.ChoiceField(
        choices=RESULT_TERM_CHOICES
    )
    results_period = forms.ChoiceField(
        choices=RESULT_PERIOD_CHOICES
    )
    UPLOAD_OPTIONS = [
        (1, "Update"),
        (2, "Print")
    ]
    option = forms.ChoiceField(
        choices=UPLOAD_OPTIONS
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        subject_passed_id = cleaned_data.get("results_subjects")
        if subject_passed_id:
            subject_passed = SubjectProfile.objects.get(subject_id = subject_passed_id)
            cleaned_data["results_subjects"] = subject_passed
        return cleaned_data


    