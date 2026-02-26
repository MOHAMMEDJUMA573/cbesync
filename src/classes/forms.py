from django import forms
from django.db import transaction
from .models import ClassProfile, ProgramProfile
from results.models import SubjectProfile
from teachers.models import TeacherProfile
from results.models import ExaminationProfile
import uuid
from .models import SchoolProfile
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _

def generate_unique_class_id():
    while True:
        new_id = f"CLS-{uuid.uuid4().hex[:16].upper()}"
        if not ClassProfile.objects.filter(class_id=new_id).exists():
            return new_id

CLASS_SUBJECTS_DICT = {
    'JSS': [('ENGL','English'), ('KISW','Kiswahili'), ('MATS','Mathematics'), ('RLED','Religious Education'), ('SSTD','Social Studies'), ('INTS','Intergrated Science'), ('PRTS','Pre-Technical'), ('AGNT','Agriculture and Nutrition'), ('CASP','Creative Arts & Sports')],
    'UPE': [('ENGL','English'), ('KISW','Kiswahili'), ('MATS','Mathematics'), ('RLED','Religious Education'), ('SSTD','Social Studies'), ('SATC','Science & Technology '), ('AGNT','Agriculture & Nutrition'), ('CASP','Creative Arts & Sports')],
    'LPE': [('ENGL','English L Activities'), ('KISW','Kiswahili L Activities'), ('MATS','Mathematics Activities'), ('RLED','Religious E. Activities'), ('ENVA','Environmental Activities'), ('CRAT','Creative Activities')],
    'PPE': [('LGAT','Language Activities'), ('MATS','Mathematical Activities'), ('CRAT','Creative Activities'), ('EVAT','Environment Activities'), ('REAT','Religious Activities')]
}
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

class ClassRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        programs_list = [
            (str(p.program_id), str(p.get_program_name_display()))
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
        min_value=50,
        max_value=300,
        widget=forms.NumberInput(
            attrs={
                "max":300,
                "min":50
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
            #create the class object
            class_saved = ClassProfile.objects.create(
                class_school = class_school,
                class_title = self.cleaned_data["class_title"],
                class_level = self.cleaned_data["class_level"],
                class_program = self.cleaned_data["class_program"],
                class_teacher = self.cleaned_data["class_teacher"],
                class_description = self.cleaned_data["class_description"],
                class_capacity = self.cleaned_data["class_capacity"],
                class_status = 'Ac' 
            )
            #create exams for the class
            if class_saved:
                for term in ExaminationProfile.EXAMINATION_TERM_CHOICES:
                    for period in ExaminationProfile.EXAMINATION_PERIOD_CHOICES:
                        ExaminationProfile.objects.create(
                            examination_school = class_school,
                            examination_class = class_saved,
                            examination_term = term[0],
                            examination_period = period[0]
                        )
                        
            #create subjects for the class
            class_program = self.cleaned_data["class_program"]
            if class_program.program_name :
                class_subjects_tuples = CLASS_SUBJECTS_DICT.get(class_program.program_name)
                for subject in class_subjects_tuples:
                    SubjectProfile.objects.create(
                        subject_class = class_saved,
                        subject_school = class_school,
                        subject_code = subject[0],
                        subject_name = subject[1],
                        subject_program = class_program,
                    )

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
     
class ClassTeacherAssignmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        classes_tuple_choices = kwargs.pop("classes_tuple_list")
        teachers_tuple_choices = kwargs.pop("teachers_tuple_list")
        super(ClassTeacherAssignmentForm, self).__init__(*args, **kwargs)
        self.fields["classes_objs"].choices = classes_tuple_choices
        self.fields["teachers_objs"].choices = teachers_tuple_choices

    classes_objs = forms.ChoiceField(
        choices=()
    )
    teachers_objs = forms.ChoiceField(
        choices=()
    )

    def clean(self):
        cleaned_data = super().clean()
        class_passed = cleaned_data.get("classes_objs")
        teacher_passed = cleaned_data.get("teachers_objs")
        if class_passed and teacher_passed:
            try:
                class_obj = ClassProfile.objects.get(class_id=class_passed)
                teacher_obj = TeacherProfile.objects.get(teacher_id=teacher_passed)
                cleaned_data["classes_objs"] = class_obj
                cleaned_data["teacher_objs"] = teacher_obj
            except (ClassProfile.DoesNotExist, TeacherProfile.DoesNotExist):
                raise forms.ValidationError("Non existent options ")
        return cleaned_data
            
    def save(self):
        with transaction.atomic():
            class_passed = self.cleaned_data["classes_objs"]
            class_passed.class_teacher = self.cleaned_data["teacher_objs"]
            class_passed.save(update_fields=["class_teacher"])