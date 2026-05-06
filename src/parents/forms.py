from django import forms
from .models import ParentProfile
from datetime import date
from phonenumber_field.formfields import PhoneNumberField
from accounts.models import CustomUser
from better_profanity import profanity
from django.utils.translation import gettext_lazy as _
from django.db import transaction
import uuid
from django.db.models import F
from django.forms.widgets import Select, FileInput


def generate_unique_parent_id():
    while True:
        new_id = f"PRT-{uuid.uuid4().hex[:16].upper()}"
        if not ParentProfile.objects.filter(parent_id=new_id).exists():
            return new_id

INPUTCSS = "flex flex-1 outline-0 p-2 rounded-md max-w-auto md:max-w-[30ch] bg-inputbg text-inputtxt border border-bordercl"

class ParentRegistrationForm(forms.Form):
    parent_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    parent_middle_name = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    parent_last_name = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )

    parent_gender = forms.ChoiceField(
        choices=ParentProfile.GENDER_CHOICES,
        widget=forms.RadioSelect,
    )
    
    parent_phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                'autocomplete':"off",
                "class":INPUTCSS
            }
        ),
        initial="+254",
    )
    parent_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off",
                "class":INPUTCSS
            }
        ),
        max_length=30,
    )
    
    parent_home_address = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class":INPUTCSS
            }
        )
    )
    parent_country = forms.ChoiceField(
        widget=Select(
            attrs={
                "class":INPUTCSS
            }
        ),
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
    )

    parent_pic = forms.ImageField(
        widget=FileInput(
            attrs={
                "class":INPUTCSS
            }
        ),
        required=False
    )

    def clean(self):
        check_flag1 = False
        cleaned_data =  super().clean()
        parent_fields = [
            "parent_first_name", "parent_middle_name", "parent_last_name",
            "parent_email"
        ]
        for parent_field in parent_fields:
            value = cleaned_data.get(parent_field)
            if value:
                if profanity.contains_profanity(value):
                    self.add_error(
                        parent_field,
                        _(f"{profanity.censor(value)} is abusive!")
                    )
                    check_flag1 = True
        if check_flag1:
            return cleaned_data
        #check for none fields
        if check_flag1:
           return cleaned_data
        parent_middle_name = cleaned_data.get("parent_middle_name")
        if not parent_middle_name:
            cleaned_data["parent_middle_name"] = ""
        #lowercase the email
        r_email = cleaned_data.get("parent_email")
        if r_email:
            email = r_email.lower()
            cleaned_data["parent_email"] = email
            if CustomUser.objects.filter(email__iexact=email).exists():
                self.add_error(
                    "parent_email",
                    _("Email already in use!")
                )

        return cleaned_data

    def save(self, parent_school, commit=True):
        with transaction.atomic():
            username = generate_unique_parent_id()
            user = CustomUser.objects.create_user(
                username=username,
                email=self.cleaned_data['parent_email'],
                password=str(username),
                user_type='parent',
                user_country = self.cleaned_data['parent_country'],
            )
            #create the parent
            ParentProfile.objects.create(
                user = user,
                parent_id = username,
                parent_pic = self.cleaned_data['parent_pic'],
                parent_school = parent_school,

                parent_first_name = (self.cleaned_data['parent_first_name']).title(),
                parent_middle_name = (self.cleaned_data['parent_middle_name']).title(),
                parent_last_name = (self.cleaned_data['parent_last_name']).title(),

                parent_gender = self.cleaned_data['parent_gender'],

                parent_phone = self.cleaned_data['parent_phone'],
                parent_email = self.cleaned_data['parent_email'],
                parent_home_address = self.cleaned_data['parent_home_address'],

                parent_status = 'A' 
            )
            
class ParentEnrollmentForm(forms.Form):
    parent_first_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )
    parent_last_name = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )

    parent_gender = forms.ChoiceField(
        choices=ParentProfile.GENDER_CHOICES,
        widget=forms.RadioSelect,
    )
    parent_id = forms.CharField(
        max_length=35,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off',
                "class":INPUTCSS
            }
        )
    )

    def clean(self):
        check_flag1 = False
        cleaned_data = super().clean()
        parent_fields = [
            "parent_first_name", "parent_last_name",
        ]
        for parent_field in parent_fields:
            value = cleaned_data.get(parent_field)
            if value:
                value = value.title()
                cleaned_data[parent_field] = value
                if profanity.contains_profanity(value):
                    self.add_error(
                        parent_field,
                        _(f"{profanity.censor(value)} is unallowed!")
                    )
                    check_flag1 = True
        if check_flag1:
            return cleaned_data

        return cleaned_data
   