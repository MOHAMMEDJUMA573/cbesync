from django.http import HttpResponse
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from allauth.account.decorators import verified_email_required
import uuid
from students.forms import StudentRegistrationForm

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#man_dashbordand subs
@verified_email_required
def dashboard(request):
    if request.user.user_type == "school":
        current_school_id = request.user.username
        if school_uuid == valid_school_uuid:
            template_name = "schools/dashl0/school_index.html"
            page_title = "S-Dashboard"

            context = {
                "page_title":page_title
            }   
    else:
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
        
    
    return render(request, template_name, context)

#usermanagement and subs
@verified_email_required
def user_management(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        template_name = "schools/dashl0/school_usermng.html"
        page_title = "Management"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
    
    return render(request, template_name, context)

def teacher_registration(request):
    if school_uuid == valid_school_uuid:
        template_name = "schools/usrmng/t_reg.html"
        page_title = "T-Management"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user management page</h1>")
    
    return render(request, template_name, context)

@verified_email_required
def student_registration(request):
    if request.user.user_type == "school":
        template_name = "schools/usrmng/s_reg.html"
        page_title = "S-Management"
        form = StudentRegistrationForm()
        if request.method == "POST":
        # if school_uuid == valid_school_uuid:
            form = StudentRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(student_school=request.user.school_profile)         


                return HttpResponse(f"Student saved:\n {form.cleaned_data}")

            context = {
                "page_title":page_title,
                "form":form
            }
        else:
            
            context = {
                "page_title":"page_title",
                "form": form
            }        
    return render(request, template_name, context)
def parent_registration(request):
    if school_uuid == valid_school_uuid:
        template_name = "schools/usrmng/p_reg.html"
        page_title = "P-Management"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user management page</h1>")
    
    return render(request, template_name, context)

def ntstaff_registration(request):
    if school_uuid == valid_school_uuid:
        template_name = "schools/usrmng/nt_reg.html"
        page_title = "NT-Management"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user management page</h1>")
    
    return render(request, template_name, context)
#class management and subs
def class_management(request):
    if school_uuid == valid_school_uuid:
        return HttpResponse(f"<h1>Right guy {school_uuid} class management</h1>")
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} class management</h1>")
