from django import forms
from.models import ResultsProfile
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _


class ResultsSubmissionForm(forms.Form):
    result_student = forms.CharField(

    )
    result_class = forms.CharField(

    )
    result_teacher = forms.CharField(

    )
    result_school = forms.CharField(

    )
    result_subject = forms.CharField(

    )
    result_score = forms.IntegerField(
        initial=0
    )
    result_term = forms.CharField(
        choices=ResultsProfile.RESULT_TERM_CHOICES
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