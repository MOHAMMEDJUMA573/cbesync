from django.http import HttpResponse
from django.contrib import messages
from students.models import StudentProfile
from teachers.models import TeacherProfile
from ntstaffs.models import NtStaffProfile
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.decorators import verified_email_required
import uuid
from teachers.forms import TeacherRegistrationForm, TeacherSearchForm, TeacherEnrollmentForm
from students.forms import StudentRegistrationForm, StudentSearchForm
from ntstaffs.forms import NtStaffRegistrationForm, NtStaffSearchForm
from parents.forms import ParentRegistrationForm
from django.db.models import Q

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#man_dashbordand subs
@verified_email_required
def dashboard(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_students_polpulation = current_school.school_students_polpulation
        school_teachers_polpulation = current_school.school_teachers_polpulation
        school_ntstaffs_polpulation = current_school.school_ntstaffs_polpulation
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
                "student_count":school_students_polpulation,
                "teacher_count":school_teachers_polpulation,
                "ntstaff_count":school_ntstaffs_polpulation,
            }   
    else:
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
        
    
    return render(request, template_name, context)

#usermanagement and subs
@verified_email_required
def user_management(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        school_name = request.user.school_profile.school_name
        template_name = "schools/dashl0/school_usermng.html"
        page_title = "Management"

        context = {
            "school_name":school_name,
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
    
    return render(request, template_name, context)

@verified_email_required
def teacher_registration(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        school_name = request.user.school_profile.school_name
        template_name = "schools/usrmng/t_reg.html"
        page_title = "T-Registration"
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
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
                return render( request, template_name, context )
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")

@verified_email_required
def teacher_enrollment(request):
    if request.user.user_type == "school":
        school_name = request.user.school_profile.school_name
        template_name = "schools/usrmng/t_enroll.html"
        page_title = "T-Enrollment"
        form = TeacherEnrollmentForm()
        if request.method == "POST":
            form = TeacherEnrollmentForm(request.POST)
            if form.is_valid():
                print("valid form")
                passed_teacher_id = form.cleaned_data["teacher_id"]
                passed_first_name = form.cleaned_data["teacher_first_name"]
                passed_last_name = form.cleaned_data["teacher_last_name"]
                try:
                    enrolled_teacher = TeacherProfile.objects.get(teacher_id=passed_teacher_id)
                    teacher_first_name = enrolled_teacher.teacher_first_name
                    teacher_last_name = enrolled_teacher.teacher_last_name
                    #check if passed values matter
                    if teacher_first_name == passed_first_name and teacher_last_name == passed_last_name:
                        messages.success(
                            request,
                            (f"Teacher {teacher_last_name} : {passed_teacher_id} enrolled successfully")
                        )
                        context = {
                            "school_name":school_name,
                            "page_title":page_title,
                            "form":form
                        }
                        return render(request, template_name, context)
                    else:
                        messages.warning(
                            request,
                            (f"First name or Last name doesn't Match")
                        )
                        context = {
                            "school_name":school_name,
                            "page_title":page_title,
                            "form":form
                        }
                        return render(request, template_name, context)
                except TeacherProfile.DoesNotExist:
                    messages.warning(
                        request,
                        (f"The ID {form.cleaned_data['teacher_id']} does not exist in the system")
                    )
                    context = {
                        "school_name":school_name,
                        "page_title":page_title,
                        "form":form
                    }
                    return render(request, template_name, context)
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
                return render(request, template_name, context)
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")

@verified_email_required
def teacher_ledger_view(request):
    if request.user.user_type == "school":
        #validate if its the right school
        school_name = request.user.school_profile.school_name
        template_name = "schools/dashl1/school_index_teachers.html"
        page_title = "T-LedgerView"
        current_school = request.user.school_profile
        school_teachers = TeacherProfile.objects.filter(teacher_school=current_school)
        form = TeacherSearchForm()
        if request.method == "POST":
        # if school_uuid == valid_school_uuid:
            form = TeacherSearchForm(request.POST)
            if form.is_valid():
                search_value = form.cleaned_data["teacher_data"]
                teacher_search_results = school_teachers.filter(
                    Q(teacher_first_name__iexact=search_value) |
                    Q(teacher_middle_name__iexact=search_value) |
                    Q(teacher_last_name__iexact=search_value) |
                    Q(teacher_id__iexact=search_value)
                )
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_teachers":school_teachers,
                    "form":form,
                    "search_results":teacher_search_results if teacher_search_results.exists() else "empty"
                }
                return render(request, template_name, context)              
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_teachers":school_teachers,
                    "form":form,
                    "search_results":None
                }
                return render(request, template_name, context)
        else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_teachers":school_teachers,
                    "form":form,
                    "search_results":None
                }
                return render(request, template_name, context)       
    else:
        return HttpResponse("Only schools are allowed bro")

@verified_email_required
def student_registration(request):
    if request.user.user_type == "school":
        school_name = request.user.school_profile.school_name
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
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
                return render( request, template_name, context )
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form": form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")

@verified_email_required
def student_enrollment(request):
    pass

@verified_email_required
def student_ledger_view(request):
    if request.user.user_type == "school":
        #validate if its the right school
        school_name = request.user.school_profile.school_name
        template_name = "schools/dashl1/school_index_students.html"
        page_title = "S-LedgerView"
        current_school = request.user.school_profile
        school_students = StudentProfile.objects.filter(student_school=current_school)
        form = StudentSearchForm()
        if request.method == "POST":
        # if school_uuid == valid_school_uuid:
            form = StudentSearchForm(request.POST)
            if form.is_valid():
                search_value = form.cleaned_data["student_data"]
                student_search_results = school_students.filter(
                    Q(student_first_name__iexact=search_value) |
                    Q(student_middle_name__iexact=search_value) |
                    Q(student_last_name__iexact=search_value) |
                    Q(student_id__iexact=search_value)
                )
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_students":school_students,
                    "form":form,
                    "search_results":student_search_results if student_search_results.exists() else "empty"
                }
                return render(request, template_name, context)
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_students":school_students,
                    "form":form,
                    "search_results":None
                }
                return render(request, template_name, context)
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "school_students":school_students,
                "form":form,
                "search_results":None
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools are allowed bro")
#school parents views
def parent_registration(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        school_name = request.user.school_profile.school_name
        template_name = "schools/usrmng/p_reg.html"
        page_title = "P-Management"
        form = ParentRegistrationForm()
        if request.method == "POST":
            form = ParentRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(parent_school=request.user.school_profile)
                messages.success(
                    request,
                    f"Parent: {form.cleaned_data['parent_first_name']} {form.cleaned_data['parent_last_name']} saved successfully! 🥳"
                ) 
                return redirect(reverse("schools:school_parent_registration"))
            else:
                context = {
                    "page_title":page_title,
                    "form":form
                }
                return render(request, template_name, context)
        else:          
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")
    
    return render(request, template_name, context)

@verified_email_required
def parent_enrollment(request):
    pass

#ntstaff views
@verified_email_required
def ntstaff_registration(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        school_name = request.user.school_profile.school_name
        template_name = "schools/usrmng/nt_reg.html"
        page_title = "NT-Management"
        form = NtStaffRegistrationForm()
        if request.method == "POST":
            form = NtStaffRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                    form.save(ntstaff_school=request.user.school_profile)     
                    messages.success(
                        request,
                        f"Non T Staff: {form.cleaned_data['ntstaff_first_name']} {form.cleaned_data['ntstaff_last_name']} saved successfully! 🥳"
                    ) 
                    return redirect(reverse("schools:school_ntstaff_registration"))
            else: 
                context = {
                    "page_title":page_title,
                    "form":form
                }
                return render(request, template_name, context)
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")
    
@verified_email_required
def ntstaff_enrollment(request):
    pass

@verified_email_required
def ntstaff_ledger_view(request):
    if request.user.user_type == "school":
        #validate if its the right school
        school_name = request.user.school_profile.school_name
        template_name = "schools/dashl1/school_index_ntstaff.html"
        page_title = "NT-LedgerView"
        current_school = request.user.school_profile
        school_ntstaffs = NtStaffProfile.objects.filter(ntstaff_school=current_school)
        school_scadmin_ntstaffs = school_ntstaffs.filter(
            ntstaff_j_title__in = ["SSCR","SBSR"]
        )
        school_scsupport_ntstaffs = school_ntstaffs.filter(
            ntstaff_j_title__in = ["SSOF","SOJT","SNSR"]
        )
        school_stsupport_ntstaffs = school_ntstaffs.filter(
            ntstaff_j_title__in = ["SLBT","SGOF"]
        )
        school_ntstaffs_dict = {
            "scadmin_ntstaffs":school_scadmin_ntstaffs if school_scadmin_ntstaffs.exists() else None,
            "scsupport_ntstaffs":school_scsupport_ntstaffs if school_scsupport_ntstaffs.exists() else None,
            "scstsupport_ntstaffs":school_stsupport_ntstaffs if school_stsupport_ntstaffs.exists() else None
        }
        form = NtStaffSearchForm()
        if request.method == "POST":
        # if school_uuid == valid_school_uuid:
            form = NtStaffSearchForm(request.POST)
            if form.is_valid():
                search_value = form.cleaned_data["ntstaff_data"]
                ntstaff_search_results = school_ntstaffs.filter(
                    Q(ntstaff_first_name__iexact=search_value) |
                    Q(ntstaff_middle_name__iexact=search_value) |
                    Q(ntstaff_last_name__iexact=search_value) |
                    Q(ntstaff_id__iexact=search_value)
                )
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form,
                    "search_results":ntstaff_search_results if ntstaff_search_results.exists() else "empty",
                    "school_ntstaff_dict":school_ntstaffs_dict
                }
                return render(request, template_name, context)
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form,
                    "search_results":None,
                    "school_ntstaff_dict":school_ntstaffs_dict
                }
                return render(request, template_name, context)
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form,
                "search_results":None,
                "school_ntstaff_dict":school_ntstaffs_dict
            }
            return render(request, template_name, context)      
    else:
        return HttpResponse("Only schools are allowed bro")

#class management and subs
def class_management(request):
    if school_uuid == valid_school_uuid:
        return HttpResponse(f"<h1>Right guy {school_uuid} class management</h1>")
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} class management</h1>")
