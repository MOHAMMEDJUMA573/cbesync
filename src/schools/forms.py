from allauth.account.forms import SignupForm
from django import forms
from .models import School

class SchoolSignupForm(SignupForm):
    # --- School fields ---
    school_code = forms.CharField(max_length=20, label="School Code")
    school_name = forms.CharField(max_length=150, label="School Name")
    school_type = forms.ChoiceField(choices=School.SCHOOL_TYPES_CHOICES)
    school_ownership = forms.ChoiceField(choices=School.OWNERSHIP_CHOICES)

    school_country = forms.CharField(max_length=20, initial="Kenya")
    school_county = forms.CharField(max_length=50)
    school_subcounty = forms.CharField(max_length=50, required=False)
    school_ward = forms.CharField(max_length=50, required=False)
    school_location = forms.CharField(max_length=255, required=False)

    school_phone = forms.CharField(max_length=20)

    def save(self, request):
        # 1️⃣ Create the user first
        user = super().save(request)
        # ✅ Assign role
        user.user_type = 'school'
        user.save(update_fields=['user_type'])

        # 2️⃣ Create the School linked to the user
        School.objects.create(
            user=user,
            school_code=self.cleaned_data['school_code'],
            school_name=self.cleaned_data['school_name'],
            school_type=self.cleaned_data['school_type'],
            school_ownership=self.cleaned_data['school_ownership'],
            school_country=self.cleaned_data['school_country'],
            school_county=self.cleaned_data['school_county'],
            school_subcounty=self.cleaned_data.get('school_subcounty'),
            school_ward=self.cleaned_data.get('school_ward'),
            school_location=self.cleaned_data.get('school_location'),
            school_phone=self.cleaned_data['school_phone'],
            school_status='Pending',  # default
        )

        return user