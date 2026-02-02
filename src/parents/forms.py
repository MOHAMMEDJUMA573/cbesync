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


def generate_unique_parent_id():
    while True:
        new_id = f"PRT-{uuid.uuid4().hex[:16].upper()}"
        if not ParentProfile.objects.filter(parent_id=new_id).exists():
            return new_id
        



class ParentRegistrationForm(forms.Form):
    parent_first_name = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    parent_middle_name = forms.CharField(
        max_length=35,
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
                }
        )
    )
    parent_last_name = forms.CharField(
        max_length=35,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'off'
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
                'autocomplete':"off"
            }
        ),
        initial="+254",
    )
    parent_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete':"off"
                }
        ),
        max_length=30,
    )
    
    parent_home_address = forms.CharField(
        max_length=50,
    )
    parent_country = forms.ChoiceField(
        choices=CustomUser.CBESYNC_COUNTRIES,
        initial="KEN",
    )

    parent_pic = forms.ImageField(
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
        #check for none fields
        if not check_flag1:
            nn_fields = [
                "parent_gender","parent_country"
            ]
            #for some future validations
        #lowercase the email
        r_email = cleaned_data.get("parent_email")
        if r_email:
            cleaned_data["parent_email"] = r_email.lower()

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

                parent_first_name = self.cleaned_data['parent_first_name'],
                parent_middle_name = self.cleaned_data['parent_middle_name'],
                parent_last_name = self.cleaned_data['parent_last_name'],

                parent_gender = self.cleaned_data['parent_gender'],

                parent_phone = self.cleaned_data['parent_phone'],
                parent_email = self.cleaned_data['parent_email'],
                parent_home_address = self.cleaned_data['parent_home_address'],

                parent_status = 'A' 
            )
            #increment the nuber of parents in the school
            parent_school.school_parents_polpulation = F(
                'school_parents_polpulation'
            ) + 1
            parent_school.save(update_fields=['school_parents_polpulation'])
            
