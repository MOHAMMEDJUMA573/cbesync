from django import forms
from django.db import transaction
from .models import ClassProfile, ProgramProfile
from teachers.models import TeacherProfile
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
    def __init__(self, *args, **kwargs):
        programs_list = [
            (str(p.program_id), str(p.program_name))
            for p in ProgramProfile.objects.all()
        ]
        teachers_list = kwargs.pop("teachers_list")

        super(ClassRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['class_teacher'].choices = teachers_list
        self.fields["class_program"].choices = programs_list

    class_title = forms.ChoiceField(
        choices=ClassProfile.CLASS_TITLES_CHOICES
    )

    class_level = forms.ChoiceField(
        choices=ClassProfile.CLASS_LEVEL_CHOICES,
        initial=13
    )

    class_program = forms.ChoiceField(
        choices=(),
        required=True
    )

    class_teacher = forms.ChoiceField(
    )

    class_capacity = forms.IntegerField(
        min_value=20,
        max_value=200,
        widget=forms.NumberInput(
            attrs={
                "max":200,
                "min":20
            }
        )
    )

    class_description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(
            attrs={
                'autocomplete':'off',
                "rows":2,
                "columns":4
            }
        )
    )
    
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
        #get the keyed fields
        teachers = cleaned_data.get('class_teacher')
        programs = cleaned_data.get('class_program')
        if not teachers or not programs:
            return cleaned_data
        cleaned_data['class_program'] = ProgramProfile.objects.get(
            program_id=self.cleaned_data['class_program']
        )
        cleaned_data['class_teacher'] = TeacherProfile.objects.get(
            teacher_id=self.cleaned_data['class_teacher']
        )

        return cleaned_data

    def save(self, class_school, commit=True):
        with transaction.atomic():
            ClassProfile.objects.create(
                class_school = class_school,
                class_title = self.cleaned_data["class_title"],
                class_level = self.cleaned_data["class_level"],
                class_program = self.cleaned_data["class_program"],
                class_teacher = self.cleaned_data["class_teacher"],
                class_description = self.cleaned_data["class_description"],
                class_capacity = self.cleaned_data["class_capacity"],
                class_status = 'Ac' 
            )
            print("class created successdyfully")

class ClassDeletionForm(forms.Form):
    class_id = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "max_length":35
            }
        )
    )

    def clean(self):
        check_flag1 = False
        cleaned_data = super().clean()
        classes_fields = [
            "class_id"
        ]
        for class_field in classes_fields:
            value = cleaned_data.get(class_field)
            if value:
                if profanity.contains_profanity(value):
                    self.add_error(
                        class_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        if not check_flag1:
            nn_fields = [
                "class_id"
            ]
            #for some future validation

        return cleaned_data
     
