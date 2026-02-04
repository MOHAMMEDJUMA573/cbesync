from django import forms
from django.db import transaction
from .models import ClassProfile
import uuid
from .models import SchoolProfile
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _

def generate_unique_class_id():
    while True:
        new_id = f"CLS-{uuid.uuid4().hex[:16].upper()}"
        if not ClassProfile.objects.filter(class_id=new_id).exists():
            return new_id

class ClassRegistrationForm(forms.Form):
    class_title = forms.ChoiceField(
        choices=ClassProfile.CLASS_TITLES_CHOICES
    )

    class_level = forms.ChoiceField(
        choices=ClassProfile.CLASS_LEVEL_CHOICES
    )

    class_program = forms.ChoiceField(
        choices=(),
        required=True
    )

    class_teacher = forms.ChoiceField(
        choices=(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        classes_list = kwargs.pop("classes_list", None)
        teachers_list = kwargs.pop("teachers_list", None)
        super().__init__(*args, **kwargs)

        if classes_list is not None:
            self.fields["class_program"].choices = classes_list
        if teachers_list is not None:
            self.fields["class_teacher"].choices = teachers_list

    

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        class_fields = [
            "class_title"
        ]
        for class_field in class_fields:
            value = cleaned_data.get(class_field)
            if value:
                if profanity.contains_profanity(value):
                    self.add_error(
                        class_field,
                        _(f"{profanity.censor(value)} is abusive!")
                    )
                    check_flag1 = True
        #check for none fields
        if not check_flag1:
            nn_fields = [
                "class_program", "class_teacher"
            ]
            #for some future validations       

        return cleaned_data

    def save(self, class_school, commit=True):
        with transaction.atomic():
            ClassProfile.objects.create(
                class_school = class_school,
                class_title = self.cleaned_data['class_title'],
                class_level = self.cleaned_data['class_level'],
                class_program = self.cleaned_data['class_program'],
                class_teacher = self.cleaned_data['class_teacher'],
                class_status = 'Ac' 
            )
            print("class created successdyfully")
