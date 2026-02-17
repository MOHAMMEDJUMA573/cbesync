from django import forms
from.models import ResultsProfile
from classes.models import ClassProfile
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _
from datetime import datetime

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
class ResultsSubmissionForm(forms.Form):
    result_student = forms.ChoiceField(

    )
    result_exam = forms.ChoiceField(
        choices=()
    )
    result_class = forms.ChoiceField(

    )
    result_teacher = forms.ChoiceField(

    )
    result_school = forms.ChoiceField(

    )
    result_subject = forms.ChoiceField(

    )
    result_score = forms.IntegerField(
        initial=0
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        results_fields = [
            "result_score"
        ]
        for result_field in results_fields:
            value = cleaned_data.get(result_field)
            if value:
                if profanity.contains_profanity(value):
                    self.add_error(
                        result_field,
                        _(f"{profanity.censor(value)} is abusive!")
                    )
                    check_flag1 = True
        #check for none fields
        if not check_flag1:
            nn_fields = [
                "result_student"
            ]
            #for some future validations
        
        return cleaned_data
    
class ResultsFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        classes_tuple_choices = kwargs.pop("classes_tuple_list")
        super(ResultsFilterForm, self).__init__(*args, **kwargs)
        self.fields["result_class"].choices = classes_tuple_choices
    
    result_class = forms.ChoiceField(
        choices = ()
    )
    result_term = forms.ChoiceField(
        choices=RESULT_TERM_CHOICES
    )
    result_period = forms.ChoiceField(
        choices=RESULT_PERIOD_CHOICES
    )
    current_year = int((datetime.today()).year)
    RESULTS_YEAR_CHOICES = [
        (str(c), c)
        for c in range((current_year-10),(current_year+10),1)
    ]
    result_year = forms.ChoiceField(
        choices=RESULTS_YEAR_CHOICES,
        initial=int((datetime.today()).year)
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
    

class TeacherResultsUploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        subjects_tuple_choices = kwargs.pop("subjects_tuple_choices")
        classes_tuple_choices = kwargs.pop("classes_tuple_choices")
        super(TeacherResultsUploadForm, self).__init__(*args, **kwargs)
        self.fields["results_subjects"].choices = subjects_tuple_choices
        self.fields["results_classes"].choices = classes_tuple_choices
    results_subjects =forms.ChoiceField(
        choices=()
    )
    results_classes = forms.ChoiceField(
        choices=()
    )
    results_terms = forms.ChoiceField(
        choices=RESULT_TERM_CHOICES
    )
    results_period = forms.ChoiceField(
        choices=RESULT_PERIOD_CHOICES
    )
    UPLOAD_OPTIONS = [
        ("update", "Update"),
        ("new", "New")
    ]
    option = forms.ChoiceField(
        choices=UPLOAD_OPTIONS
    )

    def clean(self):
        pass

    