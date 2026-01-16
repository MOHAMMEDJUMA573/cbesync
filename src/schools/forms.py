from allauth.account.forms import SignupForm
from django import forms
from .models import SchoolProfile


class SchoolSignupForm(SignupForm):
    # --- School fields ---
    school_code = forms.CharField(max_length=20, required=True, label="School Code")
    school_name = forms.CharField(max_length=150, required=True, label="School Name")
    school_badge = forms.ImageField(required=False)

    school_type = forms.ChoiceField(choices=SchoolProfile.SCHOOL_TYPES_CHOICES)
    school_ownership = forms.ChoiceField(choices=SchoolProfile.OWNERSHIP_CHOICES)

    school_country = forms.CharField(max_length=20, initial="Kenya")
    school_county = forms.CharField(max_length=50)
    school_subcounty = forms.CharField(max_length=50, required=False)
    school_ward = forms.CharField(max_length=50, required=False)
    school_location = forms.CharField(max_length=255, required=False)

    school_phone = forms.CharField(max_length=20)

    def save(self, request):
        user = super().save(request)
        user.user_type = 'school'
        user.save(update_fields=['user_type'])
        #actual school obj creation
        SchoolProfile.objects.create(
            user=user,
            school_code=self.cleaned_data['school_code'],
            school_name=self.cleaned_data['school_name'],
            school_badge=self.cleaned_data['school_badge'],
            school_type=self.cleaned_data['school_type'],
            school_ownership=self.cleaned_data['school_ownership'],
            school_country=self.cleaned_data['school_country'],
            school_county=self.cleaned_data['school_county'],
            school_subcounty=self.cleaned_data.get('school_subcounty'),
            school_ward=self.cleaned_data.get('school_ward'),
            school_location=self.cleaned_data.get('school_location'),
            school_phone=self.cleaned_data['school_phone'],
            school_status='P',  # default
        )

        return user