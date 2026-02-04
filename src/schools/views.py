from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from students.models import StudentProfile
from teachers.models import TeacherProfile
from ntstaffs.models import NtStaffProfile
from parents.models import ParentProfile
from classes.models import ClassProfile,ProgramProfile
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.decorators import verified_email_required
import uuid
from teachers.forms import TeacherRegistrationForm, TeacherSearchForm, TeacherEnrollmentForm
from students.forms import StudentRegistrationForm, StudentSearchForm, StudentEnrollmentForm
from ntstaffs.forms import NtStaffRegistrationForm, NtStaffSearchForm, NtStaffEnrollmentForm
from parents.forms import ParentRegistrationForm, ParentEnrollmentForm
from classes.forms import ClassRegistrationForm
from django.db.models import Q
from django.db.models import F

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#***--------------------***#***--------------------***
#Dashboard-school views
#***--------------------***
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
        school_polpulation = current_school.school_polpulation
        school_creation_date = current_school.school_creation_date
        school_online_days = current_school.school_online_days
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
                "school_polpulation":school_polpulation,
                "online_days":school_online_days,
                "creation_date":school_creation_date
            }   
    else:
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
        
    
    return render(request, template_name, context)

#***--------------------***#***--------------------***
#UserManagement views
#***--------------------***
@verified_email_required
def user_management(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/dashl0/school_usermng.html"
        page_title = "U-Management"
        school_polpulation = current_school.school_polpulation
        school_creation_date = current_school.school_creation_date
        school_online_days = current_school.school_online_days

        context = {
            "school_name":school_name,
            "page_title":page_title,
            "school_polpulation":school_polpulation,
            "online_days":school_online_days,
            "creation_date":school_creation_date
        }
    else:
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
    
    return render(request, template_name, context)
#***--------------------***
#Teacher-school views
#***--------------------***
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
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)

@verified_email_required
def teacher_enrollment(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/t_enroll.html"
        page_title = "T-Enrollment"
        form = TeacherEnrollmentForm()
        if request.method == "POST":
            form = TeacherEnrollmentForm(request.POST)
            if form.is_valid():
                passed_teacher_id = form.cleaned_data["teacher_id"]
                passed_first_name = form.cleaned_data["teacher_first_name"]
                passed_last_name = form.cleaned_data["teacher_last_name"]
                passed_teacher_gender = form.cleaned_data["teacher_gender"]
                passed_teacher_role = form.cleaned_data["teacher_role"]
                passed_teacher_employer = form.cleaned_data["teacher_employer"]
                passed_e_level = form.cleaned_data["teacher_e_level"]
                passed_t_subjects = form.cleaned_data["teacher_t_subjects"]
                teacher_prefix = "Mr. " if form.cleaned_data["teacher_gender"] == "M" else "Mrs. "
                try:
                    enrolled_teacher = TeacherProfile.objects.get(teacher_id=passed_teacher_id)
                    teacher_first_name = enrolled_teacher.teacher_first_name
                    teacher_last_name = enrolled_teacher.teacher_last_name
                    teacher_gender = enrolled_teacher.teacher_gender
                    teacher_old_school = enrolled_teacher.teacher_school
                    #check if passed values matter
                    if teacher_first_name == passed_first_name and teacher_last_name == passed_last_name and teacher_gender == passed_teacher_gender :
                        if enrolled_teacher.teacher_status != "T" and teacher_old_school != current_school:
                            messages.info(
                                request,
                                (f"Teacher {teacher_last_name} : {passed_teacher_id} is yet to be released from {teacher_old_school.school_name} ")
                            )
                            context = {
                                "school_name":school_name,
                                "page_title":page_title,
                                "form":form
                            }
                        else:
                            #transfer the teacher to the new school
                            with transaction.atomic():
                                enrolled_teacher.teacher_school = current_school
                                enrolled_teacher.teacher_status = "E"
                                enrolled_teacher.teacher_role = passed_teacher_role
                                enrolled_teacher.teacher_t_subjects = passed_t_subjects
                                enrolled_teacher.teacher_employer = passed_teacher_employer
                                enrolled_teacher.teacher_e_level = passed_e_level
                                teacher_old_school.school_teachers_polpulation = F(
                                    "school_teachers_polpulation"
                                ) - 1
                                current_school.school_teachers_polpulation = F(
                                    "school_teachers_polpulation"
                                ) + 1
                                # update the fields
                                enrolled_teacher.save(
                                    update_fields=[
                                        "teacher_school","teacher_status","teacher_role","teacher_t_subjects",
                                        "teacher_employer", "teacher_e_level"
                                    ]
                                )
                                teacher_old_school.save(update_fields=["school_teachers_polpulation"])
                                current_school.save(update_fields=["school_teachers_polpulation"])
                                messages.success(
                                    request,
                                    (f"Teacher {teacher_last_name} : {passed_teacher_id} enrolled successfully")
                                )
                                context = {
                                    "school_name":school_name,
                                    "page_title":page_title,
                                    "form":TeacherEnrollmentForm()
                                }
                    else:
                        messages.warning(
                            request,
                            (f"Teacher's data in inconsistent")
                        )
                        context = {
                            "school_name":school_name,
                            "page_title":page_title,
                            "form":form
                        }
                except TeacherProfile.DoesNotExist:
                    messages.warning(
                        request,
                        (f"{teacher_prefix}{passed_last_name} {passed_teacher_id}:  Doesn't exist! Check your data!")
                    )
                    context = {
                        "school_name":school_name,
                        "page_title":page_title,
                        "form":form
                    }
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)

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
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_teachers":school_teachers,
                    "form":form,
                    "search_results":None
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "school_teachers":school_teachers,
                "form":form,
                "search_results":None
            }
    else:
        return HttpResponse("Only schools are allowed bro")
    return render(request, template_name, context)

@verified_email_required
def teacher_management(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/t_manage.html"
        page_title = "T-Management"
        if request.method == "POST":
            pass
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)
#***--------------------***
#Student-school views
#***--------------------***
@verified_email_required
def student_registration(request):
    if request.user.user_type == "school":
        school_name = request.user.school_profile.school_name
        template_name = "schools/usrmng/s_reg.html"
        page_title = "S-Registration"
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
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form": form
            }
            return render(request, template_name, context)
    else:
        return HttpResponse("Only schools allowed bro!")
    return render( request, template_name, context )

@verified_email_required
def student_enrollment(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/s_enroll.html"
        page_title = "S-Enrollment"
        form = StudentEnrollmentForm()
        if request.method == "POST":
            form = StudentEnrollmentForm(request.POST)
            if form.is_valid():
                passed_student_id = form.cleaned_data["student_id"]
                passed_first_name = form.cleaned_data["student_first_name"]
                passed_last_name = form.cleaned_data["student_last_name"]
                passed_student_gender = form.cleaned_data["student_gender"]
                passed_s_needs = form.cleaned_data["student_s_needs"]
                try:
                    enrolled_student = StudentProfile.objects.get(student_id=passed_student_id)
                    student_first_name = enrolled_student.student_first_name
                    student_last_name = enrolled_student.student_last_name
                    student_gender = enrolled_student.student_gender
                    student_old_school = enrolled_student.student_school
                    #check if passed values matter
                    if student_first_name == passed_first_name and student_last_name == passed_last_name and student_gender == passed_student_gender :
                        if enrolled_student.student_status != "T" and student_old_school != current_school:
                            messages.info(
                                request,
                                (f"Student {student_last_name} : {passed_student_id} is yet to be released from {student_old_school.school_name} ")
                            )
                            context = {
                                "school_name":school_name,
                                "page_title":page_title,
                                "form":form
                            }
                        else:
                            #transfer the teacher to the new school
                            with transaction.atomic():
                                enrolled_student.student_school = current_school
                                enrolled_student.student_status = "A"
                                #enrolled_student.student_class
                                enrolled_student.student_s_needs = passed_s_needs
                                student_old_school.school_students_polpulation = F(
                                    "school_students_polpulation"
                                ) - 1
                                current_school.school_students_polpulation = F(
                                    "school_students_polpulation"
                                ) + 1
                                # update the fields
                                enrolled_student.save(
                                    update_fields=[
                                        "student_school","student_status","student_s_needs"
                                    ]
                                )
                                student_old_school.save(update_fields=["school_students_polpulation"])
                                current_school.save(update_fields=["school_students_polpulation"])
                                messages.success(
                                    request,
                                    (f"Student {student_last_name} : {passed_student_id} enrolled successfully")
                                )
                                context = {
                                    "school_name":school_name,
                                    "page_title":page_title,
                                    "form":StudentEnrollmentForm()
                                }
                    else:
                        messages.warning(
                            request,
                            (f"Student's data in inconsistent")
                        )
                        context = {
                            "school_name":school_name,
                            "page_title":page_title,
                            "form":form
                        }
                except StudentProfile.DoesNotExist:
                    messages.warning(
                        request,
                        (f"Student: {passed_last_name} {passed_student_id}:  Doesn't exist! Check your data!")
                    )
                    context = {
                        "school_name":school_name,
                        "page_title":page_title,
                        "form":form
                    }
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)

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
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "school_students":school_students,
                    "form":form,
                    "search_results":None
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "school_students":school_students,
                "form":form,
                "search_results":None
            }
    else:
        return HttpResponse("Only schools are allowed bro")
    return render(request, template_name, context)

@verified_email_required
def student_management(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/s_manage.html"
        page_title = "S-Management"
        if request.method == "POST":
            pass
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)
#***--------------------***
#Parent-school views
#***--------------------***
@verified_email_required
def parent_registration(request):
    if request.user.user_type == "school":
    # if school_uuid == valid_school_uuid:
        school_name = request.user.school_profile.school_name
        template_name = "schools/usrmng/p_reg.html"
        page_title = "P-Registration"
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
        else:          
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)
    
@verified_email_required
def parent_enrollment(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/p_enroll.html"
        page_title = "P-Enrollment"
        form = ParentEnrollmentForm()
        if request.method == "POST":
            form = ParentEnrollmentForm(request.POST)
            if form.is_valid():
                passed_parent_id = form.cleaned_data["parent_id"]
                passed_first_name = form.cleaned_data["parent_first_name"]
                passed_last_name = form.cleaned_data["parent_last_name"]
                passed_parent_gender = form.cleaned_data["parent_gender"]
                try:
                    enrolled_parent = ParentProfile.objects.get(parent_id=passed_parent_id)
                    parent_first_name = enrolled_parent.parent_first_name
                    parent_last_name = enrolled_parent.parent_last_name
                    parent_gender = enrolled_parent.parent_gender
                    parent_old_school = enrolled_parent.parent_school
                    #check if passed values matter
                    if parent_first_name == passed_first_name and parent_last_name == passed_last_name and parent_gender == passed_parent_gender :
                         #transfer the teacher to the new school
                        with transaction.atomic():
                            enrolled_parent.parent_school = current_school
                            parent_old_school.school_parents_polpulation = F(
                                "school_parents_polpulation"
                            ) - 1
                            current_school.school_parents_polpulation = F(
                                "school_parents_polpulation"
                            ) + 1
                            #update the fields
                            enrolled_parent.save(
                                update_fields=[
                                    "parent_school"
                                ]
                            )
                            parent_old_school.save(update_fields=["school_parents_polpulation"])
                            current_school.save(update_fields=["school_parents_polpulation"])
                            messages.success(
                                request,
                                (f"Parent {parent_last_name} : {passed_parent_id} responsibility transferred from {parent_old_school.school_name} from {current_school.school_name} ")
                            )
                            context = {
                                "school_name":school_name,
                                "page_title":page_title,
                                "form":form
                            }
                    else:
                        messages.warning(
                            request,
                            (f"Parent's data in inconsistent")
                        )
                        context = {
                            "school_name":school_name,
                            "page_title":page_title,
                            "form":form
                        }
                except ParentProfile.DoesNotExist:
                    messages.warning(
                        request,
                        (f"Parent: {passed_last_name} {passed_parent_id}:  Doesn't exist! Check your data!")
                    )
                    context = {
                        "school_name":school_name,
                        "page_title":page_title,
                        "form":form
                    }
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro")
    return render(request, template_name, context)

@verified_email_required
def parent_management(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/p_manage.html"
        page_title = "P-Management"
        if request.method == "POST":
            pass
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)
#***--------------------***
#NT-Staff-school views
#***--------------------***
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
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)
    
@verified_email_required
def ntstaff_enrollment(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/nt_enroll.html"
        page_title = "NT-Enrollment"
        form = NtStaffEnrollmentForm()
        if request.method == "POST":
            form = NtStaffEnrollmentForm(request.POST)
            if form.is_valid():
                passed_ntstaff_id = form.cleaned_data["ntstaff_id"]
                passed_first_name = form.cleaned_data["ntstaff_first_name"]
                passed_last_name = form.cleaned_data["ntstaff_last_name"]
                passed_ntstaff_gender = form.cleaned_data["ntstaff_gender"]
                passed_h_qualification = form.cleaned_data["ntstaff_h_qualification"]
                passed_s_field = form.cleaned_data["ntstaff_s_field"]
                passed_y_experience = form.cleaned_data["ntstaff_y_experience"]
                passed_j_title = form.cleaned_data["ntstaff_j_title"]
                try:
                    enrolled_ntstaff = NtStaffProfile.objects.get(ntstaff_id=passed_ntstaff_id)
                    ntstaff_first_name = enrolled_ntstaff.ntstaff_first_name
                    ntstaff_last_name = enrolled_ntstaff.ntstaff_last_name
                    ntstaff_gender = enrolled_ntstaff.ntstaff_gender
                    ntstaff_old_school = enrolled_ntstaff.ntstaff_school
                    #check if passed values matter
                    if ntstaff_first_name == passed_first_name and ntstaff_last_name == passed_last_name and ntstaff_gender == passed_ntstaff_gender :
                        if enrolled_ntstaff.ntstaff_status != "T" and ntstaff_old_school != current_school:
                            messages.info(
                                request,
                                (f"Ntstaff {ntstaff_last_name} : {passed_ntstaff_id} is yet to be released from {ntstaff_old_school.school_name} ")
                            )
                            context = {
                                "school_name":school_name,
                                "page_title":page_title,
                                "form":form
                            }
                        else:
                            with transaction.atomic():
                                enrolled_ntstaff.ntstaff_school = current_school
                                enrolled_ntstaff.ntstaff_h_qualification = passed_h_qualification
                                enrolled_ntstaff.ntstaff_s_field = passed_s_field
                                enrolled_ntstaff.ntstaff_y_experience = passed_y_experience
                                enrolled_ntstaff.ntstaff_j_title = passed_j_title
                                ntstaff_old_school.school_ntstaffs_polpulation = F(
                                    "school_ntstaffs_polpulation"
                                ) - 1
                                current_school.school_ntstaffs_polpulation = F(
                                    "school_ntstaffs_polpulation"
                                ) + 1
                                #update the fields
                                enrolled_ntstaff.save(
                                    update_fields=[
                                        "ntstaff_school","ntstaff_h_qualification", "ntstaff_s_field", 
                                        "ntstaff_y_experience", "ntstaff_j_title"
                                    ]
                                )
                                ntstaff_old_school.save(update_fields=["school_ntstaffs_polpulation"])
                                current_school.save(update_fields=["school_ntstaffs_polpulation"])
                                messages.success(
                                    request,
                                    (f"NTstaff {ntstaff_last_name} : {passed_ntstaff_id} enrolled successfully")
                                )
                                context = {
                                    "school_name":school_name,
                                    "page_title":page_title,
                                    "form":form
                                }
                    else:
                        messages.warning(
                            request,
                            (f"Ntstaff's data in inconsistent")
                        )
                        context = {
                            "school_name":school_name,
                            "page_title":page_title,
                            "form":form
                        }
                except NtStaffProfile.DoesNotExist:
                    messages.warning(
                        request,
                        (f"NTstaff: {passed_last_name} {passed_ntstaff_id}:  Doesn't exist! Check your data!")
                    )
                    context = {
                        "school_name":school_name,
                        "page_title":page_title,
                        "form":form
                    }
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro")
    return render(request, template_name, context)

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
            else:
                context = {
                    "school_name":school_name,
                    "page_title":page_title,
                    "form":form,
                    "search_results":None,
                    "school_ntstaff_dict":school_ntstaffs_dict
                }
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form,
                "search_results":None,
                "school_ntstaff_dict":school_ntstaffs_dict
            }
    else:
        return HttpResponse("Only schools are allowed bro")
    return render(request, template_name, context)

@verified_email_required
def ntstaff_management(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/usrmng/nt_manage.html"
        page_title = "NT-Management"
        if request.method == "POST":
            pass
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)
#***--------------------***#***--------------------***
#Class-school views
#***--------------------***
prog_list = []
all_programs = ProgramProfile.objects.all()
for prog in all_programs:
    prog_list.append(
        (f"{prog.program_id}", f"{prog.program_name}")
    )
@verified_email_required
def class_management(request):
    if request.user.user_type == "school":
        current_school = request.user.school_profile
        school_name = current_school.school_name
        template_name = "schools/dashl0/school_classmng.html"
        page_title = "C-Management"
        # classes_list = current_school.school_classes_list
        teachers_list = current_school.school_classt_list
        programs_list = prog_list
        print(programs_list)
        form = ClassRegistrationForm(teachers_list=teachers_list, programs_list=programs_list) 
        if request.method == "POST":
            form = ClassRegistrationForm(request.POST)
            print(form)
        else:
            context = {
                "school_name":school_name,
                "page_title":page_title,
                "form":form
            }
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)

