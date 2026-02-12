from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from allauth.account.decorators import verified_email_required
from django.utils.translation import gettext_lazy as _
import uuid

valid_teacher_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
teacher_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#functions to get items
def get_teacher_object(user_passed):
    return user_passed.teacher_profile

#***--------------------***#***--------------------***
#Dashboard-school views
#***--------------------***
@verified_email_required
def dashboard(request):
    if request.user.user_type == "teacher":
        current_teacher = get_teacher_object(request.user)
        if teacher_uuid == valid_teacher_uuid:
            template_name = "teachers/dashl0/teacher_index.html"
            page_title = "T-Dashboard"
            context = {
                "page_title":page_title,
                "teacher":current_teacher
            }
        else:
            return HttpResponse("Wrong teacher trying to access the page!")
    else:
        return HttpResponse("Only teachers allowed bro!")
    return render(request, template_name, context)
