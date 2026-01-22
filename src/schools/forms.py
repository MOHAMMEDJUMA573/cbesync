from allauth.account.forms import SignupForm
from django import forms
import uuid
from accounts.models import CustomUser
from .models import SchoolProfile
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#function to generate random school id
def generate_unique_school_id():
    while True:
        new_id = f"SCH-{uuid.uuid4().hex[:12].upper()}"
        if not SchoolProfile.objects.filter(school_id=new_id).exists():
            return new_id

# --- Reusable validator for school code format ---
def alphanumeric_validator(value):
    if not value.isalnum():
        raise ValidationError(
            _("School code '%(value)s' must be alphanumeric"),
            params={"value": value},
        )

class SchoolSignupForm(SignupForm):
    # --- School Form fields ---
    school_code = forms.CharField(
        max_length=20,
        required=True,
        label="School Code",
        validators=[alphanumeric_validator],
        error_messages={
            "required": _("Please enter your school code"),
            "max_length": _("School code cannot exceed 20 characters"),
            "invalid": _("School code is not valid")
        },
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    school_name = forms.CharField(
        required=True,
        max_length=150,
        label="School Name",
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    school_badge = forms.ImageField(
        required=False
    )

    school_type = forms.ChoiceField(
        initial='D',
        choices=SchoolProfile.SCHOOL_TYPES_CHOICES
    )
    school_ownership = forms.ChoiceField(
        initial='GOVT',
        choices=SchoolProfile.OWNERSHIP_CHOICES
    )

    school_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
        disabled=True,
    )
    school_admin_level_1 = forms.ChoiceField(
        initial="Coast",
        choices=SchoolProfile.KENYA_PRV_CBESYNC,
        label="State / Province / Region",
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    school_admin_level_2 = forms.ChoiceField(
        choices=SchoolProfile.KENYA_CNT_CBESYNC,
        label="County / District / Prefecture",
        initial="Mombasa",
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    school_admin_level_3 = forms.CharField(
        max_length=100,
        label="Ward / Municipality / Commune",
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    school_locality = forms.CharField(
        max_length=255,
        label="Village / Town / Neighborhood",
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )

    school_phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off"
                }
        ),
        initial="+254",
        label="Mobile No",
    )
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("school_country"):
            cleaned_data["school_country"] = "KEN"
        school_fields = [
            "school_code", "school_name", "school_type", "school_ownership",
            "school_country", "school_admin_level_1", "school_admin_level_2",
            "school_admin_level_3", "school_locality", "school_phone"
        ]        
        for school_field in school_fields:
            if not cleaned_data.get(school_field):
                return cleaned_data           
            
        school_code = cleaned_data.get("school_code")
        if SchoolProfile.objects.filter(school_code__iexact=school_code).exists():
            self.add_error(
                "school_code",
                _("This school code is already in use. Please contact CbeSync.")
            )
        
        return cleaned_data
            


    #shown full form error no specifics
    # def clean_school_code(self):
    #     code = self.cleaned_data.get("school_code")
    #     if SchoolProfile.objects.filter(school_code=code).exists():
    #         raise forms.ValidationError(
    #             _("This school code is already in use. Please contact your administrator.")
    #         )
    #     return code

    def save(self, request):
        user = super().save(request)
        username = generate_unique_school_id()
        user.user_type = 'school'
        user.username = username
        user.user_country = self.cleaned_data['school_country']
        user.save(update_fields=['user_type', 'username', 'user_country'])
        print(request.FILES)
        #actual school obj creation
        SchoolProfile.objects.create(
            user=user,
            school_code=self.cleaned_data['school_code'].upper(),
            school_name=self.cleaned_data['school_name'].upper(),
            school_badge=self.cleaned_data['school_badge'],
            school_type=self.cleaned_data['school_type'],
            school_ownership=self.cleaned_data['school_ownership'],
            school_admin_level_1=self.cleaned_data['school_admin_level_1'],
            school_admin_level_2=self.cleaned_data.get('school_admin_level_2'),
            school_admin_level_3=self.cleaned_data.get('school_admin_level_3').upper(),
            school_locality=self.cleaned_data.get('school_locality').upper(),
            school_phone=self.cleaned_data['school_phone'],
            school_status='P',  # default
        )
        print(self.cleaned_data['school_phone'])

        return user