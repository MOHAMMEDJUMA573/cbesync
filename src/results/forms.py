from django import forms
from.models import ResultsProfile
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class ResultsSubmissionForm(forms.Form):
    result_student = forms.ChoiceField(

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
    result_term = forms.ChoiceField(
        choices=ResultsProfile.RESULT_TERM_CHOICES
    )
    result_period = forms.ChoiceField(
        choices=ResultsProfile.RESULT_PERIOD_CHOICES,
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
        choices=ResultsProfile.RESULT_TERM_CHOICES
    )
    result_period = forms.ChoiceField(
        choices=ResultsProfile.RESULT_PERIOD_CHOICES,
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
    
  