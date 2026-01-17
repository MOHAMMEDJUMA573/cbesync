from allauth.account.forms import SignupForm
from django import forms
from accounts.models import CustomUser
from .models import SchoolProfile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        label="School Code",
        validators=[alphanumeric_validator],
        error_messages={
            "required": _("Please enter your school code"),
            "max_length": _("School code cannot exceed 20 characters"),
            "invalid": _("School code is not valid")
        }
    )
    school_name = forms.CharField(
        max_length=150,
        label="School Name"
    )
    school_badge = forms.ImageField(required=False)

    school_type = forms.ChoiceField(choices=SchoolProfile.SCHOOL_TYPES_CHOICES)
    school_ownership = forms.ChoiceField(choices=SchoolProfile.OWNERSHIP_CHOICES)

    school_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
        disabled=True,
    )
    school_admin_level_1 = forms.ChoiceField(
        choices=SchoolProfile.KENYA_PRV_CBESYNC,
        label="State / Province / Region",
    )
    school_admin_level_2 = forms.ChoiceField(
        choices=SchoolProfile.KENYA_CNT_CBESYNC,
        label="County / District / Prefecture",
        initial="MBS"
    )
    school_admin_level_3 = forms.CharField(
        max_length=100,
        label="Ward / Municipality / Commune",
    )
    school_locality = forms.CharField(
        max_length=255,
        label="Village / Town / Neighborhood",
    )

    school_phone = forms.CharField(max_length=20)

    #clean school_code
    def clean_school_code(self):
        code = self.cleaned_data.get("school_code")
        if SchoolProfile.objects.filter(school_code=code).exists():
            raise forms.ValidationError(
                _("This school code is already in use. Please contact your administrator.")
            )
        return code

    def save(self, request):
        user = super().save(request)
        user.user_type = 'school'
        user.user_country = self.cleaned_data['school_country']
        user.save(update_fields=['user_type', 'user_country'])
        print(request.FILES)
        #actual school obj creation
        SchoolProfile.objects.create(
            user=user,
            school_code=self.cleaned_data['school_code'],
            school_name=self.cleaned_data['school_name'],
            school_badge=self.cleaned_data['school_badge'],
            school_type=self.cleaned_data['school_type'],
            school_ownership=self.cleaned_data['school_ownership'],
            school_admin_level_1=self.cleaned_data['school_admin_level_1'],
            school_admin_level_2=self.cleaned_data.get('school_admin_level_2'),
            school_admin_level_3=self.cleaned_data.get('school_admin_level_3'),
            school_locality=self.cleaned_data.get('school_locality'),
            school_phone=self.cleaned_data['school_phone'],
            school_status='P',  # default
        )

        return user