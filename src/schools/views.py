from django.http import HttpResponse
from django.contrib import messages
from schools.models import SchoolProfile
from students.models import StudentProfile
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.decorators import verified_email_required
import uuid
from teachers.forms import TeacherRegistrationForm
from students.forms import StudentRegistrationForm

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#man_dashbordand subs
@verified_email_required
def dashboard(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_students_polpulation = current_school.school_students_polpulation
        school_teachers_polpulation = current_school.school_teachers_polpulation
        school_name = current_school.school_name
        school_id = current_school.school_id
        school_country = current_school.user.get_user_country_display()
        school_type = current_school.get_school_type_display()
        school_county = current_school.get_school_admin_level_2_display()
        if school_uuid == valid_school_uuid:
            template_name = "schools/dashl0/school_index.html"
            page_title = "S-Dashboard"

            context = {
                "page_title":page_title,
                "school_name":school_name,
                "school_id":school_id,
                "school_country":school_country,
                "school_county":school_county,
                "school_type":school_type,
                "student_count": school_students_polpulation,
                "teacher_count":school_teachers_polpulation,
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

@verified_email_required
def teacher_registration(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        template_name = "schools/usrmng/t_reg.html"
        page_title = "T-Management"
        form = TeacherRegistrationForm()
        if request.method == "POST":
            form = TeacherRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(teacher_school=request.user.school_profile)
                messages.success(
                    request,
                    f"Teacher: {form.cleaned_data['teacher_first_name']} {form.cleaned_data['teacher_last_name']} saved successfully! 🥳"
                )
                return redirect(reverse("schools:school_teacher_registration"))
        else:
            context = {
                "page_title":page_title,
                "form":form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")

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
                messages.success(
                    request,
                    f"student: {form.cleaned_data['student_first_name']} {form.cleaned_data['student_last_name']} saved successfully! 🥳"
                ) 
                return redirect(reverse("schools:school_student_registration"))
        else:
            context = {
                "page_title":page_title,
                "form": form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")

@verified_email_required
def student_ledger_view(request):
    if request.user.user_type == "school":
        #validate if its the right school
        template_name = "schools/dashl1/school_index_students.html"
        page_title = "S-LedgerView"

        current_school = request.user.school_profile
        school_students = StudentProfile.objects.filter(student_school=current_school)
        context = {
            "page_title":page_title,
            "school_students":school_students
        }
        return render(request, template_name, context)

    else:
        return HttpResponse("Only schools are allowed bro")
#school parents views
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
