from django import forms
from .models import NtStaffProfile
from datetime import date
from phonenumber_field.formfields import PhoneNumberField
from accounts.models import CustomUser
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _
from django.db import transaction
import uuid
from django.db.models import F


def generate_unique_ntstaff_id():
    while True:
        new_id = f"NTS-{uuid.uuid4().hex[:16].upper()}"
        if not NtStaffProfile.objects.filter(ntstaff_id=new_id).exists():
            return new_id
        



class NtStaffRegistrationForm(forms.Form):
    ntstaff_first_name = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    ntstaff_middle_name = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    ntstaff_last_name = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )

    ntstaff_gender = forms.ChoiceField(
        choices=NtStaffProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    ntstaff_dob = forms.DateField(
        initial=date(2001, 1, 1).strftime('%Y-%m-%d'),
    )
    
    ntstaff_phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off"
                }
        ),
        initial="+254",
    )
    ntstaff_e_contact = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off"
                }
        ),
        initial="+254",
    )
    ntstaff_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off"
                }
        ),
        max_length=30,
    )
    ntstaff_home_address = forms.CharField(
        max_length=50,
        required=True
    )

    ntstaff_h_qualification = forms.ChoiceField(
        choices=NtStaffProfile.QUALIFICATIONS,
        initial="UDGR"
    )
    ntstaff_s_field = forms.ChoiceField(
        choices=NtStaffProfile.NT_STUDY_FIELD,
        initial="INFT"
    )
    ntstaff_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
    )

    ntstaff_y_experience = forms.IntegerField(
        initial=0,
        # validators=[MaxValueValidator(60), MinValueValidator(0)],
        help_text="years of experience"
    )
    ntstaff_j_title = forms.ChoiceField(
        choices=NtStaffProfile.JOB_TITLE,
        initial="SLBT",
    )
    ntstaff_e_notes = forms.CharField(
        max_length=200,
        required=False
    )
    ntstaff_allergies = forms.MultipleChoiceField(
        choices=NtStaffProfile.ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    ntstaff_pic = forms.ImageField(
        required=False
    )

    def clean(self):
        cleaned_data =  super().clean()
        ntstaff_fields = [
            "ntstaff_first_name", "ntstaff_middle_name", "ntstaff_last_name",
            "ntstaff_email"
        ]
        for ntstaff_field in ntstaff_fields:
            value = cleaned_data.get(ntstaff_field).lower()
            if profanity.contains_profanity(value):
                self.add_error(
                    ntstaff_field,
                    _(f"{value} is unallowed!")
                )


        return cleaned_data

    def save(self, ntstaff_school, commit=True):
        with transaction.atomic():
            username = generate_unique_ntstaff_id()
            user = CustomUser.objects.create_user(
                username=username,
                email=self.cleaned_data['ntstaff_email'],
                password=str(username),
                user_type='ntstaff',
                user_country = self.cleaned_data['ntstaff_country'],
            )
            #create the ntstaff
            NtStaffProfile.objects.create(
                user = user,
                ntstaff_id = username,
                ntstaff_pic = self.cleaned_data['ntstaff_pic'],
                ntstaff_school = ntstaff_school,

                ntstaff_first_name = self.cleaned_data['ntstaff_first_name'],
                ntstaff_middle_name = self.cleaned_data['ntstaff_middle_name'],
                ntstaff_last_name = self.cleaned_data['ntstaff_last_name'],

                ntstaff_gender = self.cleaned_data['ntstaff_gender'],
                ntstaff_dob = self.cleaned_data['ntstaff_dob'],

                ntstaff_phone = self.cleaned_data['ntstaff_phone'],
                ntstaff_email = self.cleaned_data['ntstaff_email'],
                ntstaff_home_address = self.cleaned_data['ntstaff_home_address'],
                ntstaff_e_contact = self.cleaned_data['ntstaff_e_contact'],

                ntstaff_h_qualification = self.cleaned_data['ntstaff_h_qualification'],
                ntstaff_s_field = self.cleaned_data['ntstaff_s_field'],
                ntstaff_y_experience = self.cleaned_data['ntstaff_y_experience'],
                ntstaff_j_title = self.cleaned_data['ntstaff_j_title'],

                ntstaff_e_notes = self.cleaned_data['ntstaff_e_notes'],
                ntstaff_allergies = self.cleaned_data['ntstaff_allergies'],

                ntstaff_status = 'E' #ntstaff status default field
            )
            #increment the nuber of ntstaffs in the school
            ntstaff_school.school_ntstaffs_polpulation = F(
                'school_ntstaffs_polpulation'
            ) + 1
            ntstaff_school.save(update_fields=['school_ntstaffs_polpulation'])
            
