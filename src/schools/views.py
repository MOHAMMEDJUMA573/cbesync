from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from .models import SchoolProfile
from students.models import StudentProfile
from teachers.models import TeacherProfile
from ntstaffs.models import NtStaffProfile
from parents.models import ParentProfile
from classes.models import ClassProfile,ProgramProfile
from results.models import ExaminationProfile
from reports.models import StudentEReportProfile
from subjects.models import SubjectProfile
from results.models import ResultsProfile
from reports.views import student_report1_generator, student_ledger_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.decorators import verified_email_required
import uuid
from .forms import SchoolLocksForm
from teachers.forms import TeacherRegistrationForm, TeacherSearchForm, TeacherEnrollmentForm
from students.forms import StudentRegistrationForm, StudentSearchForm, StudentEnrollmentForm
from ntstaffs.forms import NtStaffRegistrationForm, NtStaffSearchForm, NtStaffEnrollmentForm
from parents.forms import ParentRegistrationForm, ParentEnrollmentForm
from classes.forms import ClassRegistrationForm, ClassDeletionForm, ClassTeacherAssignmentForm
from results.forms import ResultsFilterForm
from subjects.forms import SubjectTeacherAllocationForm
from django.db.models import Q
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Prefetch, OuterRef, Subquery

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#functions to get items
def get_school_object(user_passed):
    """Return the school object from the user
    """
    return user_passed.school_profile

def get_student_objects(passed_school):
    return StudentProfile.objects.filter(student_school=passed_school)

def get_searched_students(students_objects, search_value):
    found_students = students_objects.filter(
        Q(student_first_name__iexact=search_value) |
        Q(student_middle_name__iexact=search_value) |
        Q(student_last_name__iexact=search_value) |
        Q(student_id__iexact=search_value)
    )
    return found_students

def get_specific_student(passed_student_id):
    return StudentProfile.objects.get(student_id=passed_student_id)

def get_class_objects(passed_school):
    return ClassProfile.objects.filter(class_school=passed_school)

def get_filtered_classes(passed_classes, passed_option):
    found_classes = passed_classes.filter(
        class_title = passed_option
    )
    return found_classes

def set_filtered_class(passed_class):
    return passed_class if passed_class.exists() else None

def get_specific_class(passed_class_id):
    return ClassProfile.objects.get(class_id=passed_class_id)
    
def get_teacher_objects(passed_school):
    return TeacherProfile.objects.filter(teacher_school=passed_school)

def get_specific_teacher(passed_teacher_id):
    return TeacherProfile.objects.get(teacher_id=passed_teacher_id)

def get_teacher_choice_tuple(passed_school):
    return [
        (str(t.teacher_id), str(t.teacher_full_name))
        for t in TeacherProfile.objects.filter(teacher_school=passed_school)
    ]

def get_teacher_choice_tuple2(passed_school):
    return [
        (str(t.teacher_id), str(f"{t.teacher_first_name} {t.teacher_middle_name} {t.teacher_last_name} {t.teacher_id}"))
        for t in TeacherProfile.objects.filter(teacher_school=passed_school)
    ]

def get_ntstaff_objects(passed_school):
    return NtStaffProfile.objects.filter(ntstaff_school=passed_school)

def get_filtered_ntstaff(passed_ntstaff, passed_option):
    filtered_nstaffs = passed_ntstaff.filter(
            ntstaff_j_title__in = passed_option
    )
    return filtered_nstaffs

def set_filtered_ntstaff(passed_ntstaff):
    return passed_ntstaff if passed_ntstaff.exists() else None

def get_searched_ntstaffs(passed_ntstaffs, search_value):
    found_ntstaffs = passed_ntstaffs.filter(
        Q(ntstaff_first_name__iexact=search_value) |
        Q(ntstaff_middle_name__iexact=search_value) |
        Q(ntstaff_last_name__iexact=search_value) |
        Q(ntstaff_id__iexact=search_value)
    )
    return found_ntstaffs

def get_specific_ntstaff(passed_ntstaff_id):
    return NtStaffProfile.objects.get(ntstaff_id=passed_ntstaff_id)

def get_specific_parent(passed_parent_id):
    return ParentProfile.objects.get(parent_id=passed_parent_id)

def get_subject_choice_tuple(passed_school):
    return [
        (s.subject_id, str(s.subject_str_full))
        for s in SubjectProfile.objects.filter(subject_school=passed_school)
    ]

#***--------------------***#***--------------------***
#Dashboard-school views
#***--------------------***
@verified_email_required
def dashboard(request):
    if request.user.user_type != "school":
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    school_country = current_school.user.get_user_country_display()
    school_type = current_school.get_school_type_display()
    school_county = current_school.get_school_admin_level_2_display()
    programs = ProgramProfile.objects.all()
    template_name = "schools/dashl0/school_index.html"
    page_title = "S-Dashboard"
    context = {
        "school":current_school,
        "page_title":page_title,
        "school_country":school_country,
        "school_county":school_county,
        "school_type":school_type,
        "programmes":programs
    }       
    return render(request, template_name, context)

#***--------------------***#***--------------------***
#UserManagement views
#***--------------------***
@verified_email_required
def user_management(request):
    if request.user.user_type != "school":
        return HttpResponse(f"<h1>Wrong guy you have to be a school for this page</h1>")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school =  get_school_object(request.user)
    template_name = "schools/dashl0/school_usermng.html"
    page_title = "U-Management"
    context = {
        "school":current_school,
        "page_title":page_title
    }    
    return render(request, template_name, context)
#***--------------------***
#Teacher-school views
#***--------------------***
@verified_email_required
def teacher_registration(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school =  get_school_object(request.user)
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
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }
    return render(request, template_name, context)

@verified_email_required
def teacher_enrollment(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/t_enroll.html"
    page_title = "T-Enrollment"
    form = TeacherEnrollmentForm()
    if request.method == "POST":
        form = TeacherEnrollmentForm(request.POST)
        if form.is_valid():
            passed_teacher_id = form.cleaned_data["teacher_id"]
            passed_first_name = form.cleaned_data["teacher_first_name"]
            passed_last_name = form.cleaned_data["teacher_last_name"]
            passed_teacher_email =  form.cleaned_data["teacher_email"]
            passed_teacher_role = form.cleaned_data["teacher_role"]
            passed_teacher_phone = form.cleaned_data["teacher_phone"]
            passed_e_level = form.cleaned_data["teacher_e_level"]
            passed_t_subjects = form.cleaned_data["teacher_t_subjects"]
            try:
                enrolled_teacher = TeacherProfile.objects.get(teacher_id=passed_teacher_id)
                teacher_first_name = enrolled_teacher.teacher_first_name
                teacher_last_name = enrolled_teacher.teacher_last_name
                teacher_old_school = enrolled_teacher.teacher_school
                teacher_prefix = "Mr. " if enrolled_teacher.teacher_gender == "M" else "Mrs. "
                #check if passed values matter
                if teacher_first_name == passed_first_name and teacher_last_name == passed_last_name:
                    if enrolled_teacher.teacher_status != "T" and teacher_old_school != current_school:
                        messages.info(
                            request,
                            (f"{teacher_prefix} {teacher_last_name} : {passed_teacher_id} is yet to be released from {teacher_old_school.school_name} ")
                        )
                        context = {
                            "school":current_school,
                            "page_title":page_title,
                            "form":form
                        }
                    else:
                        #transfer the teacher to the new school
                        with transaction.atomic():
                            enrolled_teacher.teacher_school = current_school
                            enrolled_teacher.teacher_status = "E"
                            enrolled_teacher.teacher_email = passed_teacher_email
                            enrolled_teacher.teacher_phone = passed_teacher_phone
                            enrolled_teacher.teacher_role = passed_teacher_role
                            enrolled_teacher.teacher_t_subjects = passed_t_subjects
                            enrolled_teacher.teacher_e_level = passed_e_level
                            #change teacher user email too
                            user = enrolled_teacher.user
                            user.email = passed_teacher_email
                            # update the fields
                            user.save(
                                update_fields=[
                                    "email"
                                ]
                            )
                            enrolled_teacher.save(
                                update_fields=[
                                    "teacher_school","teacher_status","teacher_email","teacher_phone","teacher_role","teacher_t_subjects",
                                    "teacher_e_level"
                                ]
                            )
                            messages.success(
                                request,
                                (f"{teacher_prefix} {teacher_last_name} : {passed_teacher_id} (updated/enrolled) successfully")
                            )
                            context = {
                                "school":current_school,
                                "page_title":page_title,
                                "form":TeacherEnrollmentForm()
                            }
                else:
                    messages.warning(
                        request,
                        (f"Teacher's data in inconsistent")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form
                    }
            except TeacherProfile.DoesNotExist:
                messages.warning(
                    request,
                    (f"Mr./Mrs. {passed_last_name} {passed_teacher_id}:  Doesn't exist! Check your data!")
                )
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }
    return render(request, template_name, context)

@verified_email_required
def teacher_ledger_view(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/dashl1/school_index_teachers.html"
    page_title = "T-LedgerView"
    school_teachers = TeacherProfile.objects.filter(teacher_school=current_school)
    form = TeacherSearchForm()
    if request.method == "POST":
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
                "page_title":page_title,
                "school_teachers":school_teachers,
                "form":form,
                "search_results":teacher_search_results if teacher_search_results.exists() else "empty"
            }
        else:
            context = {
                "page_title":page_title,
                "school_teachers":school_teachers,
                "form":form,
                "search_results":None
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "school_teachers":school_teachers,
            "form":form,
            "search_results":None
        }
    return render(request, template_name, context)

@verified_email_required
def teacher_management(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/t_manage.html"
    page_title = "T-Management"
    if request.method == "POST":
        pass
    else:
        context = {
            "school":current_school,
            "page_title":page_title
        }
    return render(request, template_name, context)

@verified_email_required
def teacher_management_class_assignment(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/tmanagement/class_assignment.html"
    page_title = "T-Management"
    classes_list = current_school.school_classes_list
    teachers_list = get_teacher_choice_tuple2(current_school)
    school_teachers = get_teacher_objects(current_school)
    form = ClassTeacherAssignmentForm(classes_tuple_list=classes_list,teachers_tuple_list=teachers_list)
    if request.method == "POST":
        form = ClassTeacherAssignmentForm(request.POST,classes_tuple_list=classes_list,teachers_tuple_list=teachers_list)
        if form.is_valid():
            ct_assinged = form.cleaned_data["teacher_objs"]
            form.save()
            messages.success(
                request,
                _(f" {'Mr.' if ct_assinged.teacher_gender == 'M' else 'Ms.' } {ct_assinged.teacher_last_name} is now a class teacher🥳")
            )
            return redirect("schools:school_teacher_management_class_assignment")
        else: 
          context={
            "form":form,
            "school":current_school,
            "page_title":page_title,
            "teachers": school_teachers 
          }
    else:
        context = {
            "form":form,
            "school":current_school,
            "page_title":page_title,
            "teachers": school_teachers
        }
    return render(request, template_name, context)

@verified_email_required
def teacher_management_subject_allocation(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/tmanagement/subject_allocation.html"
    page_title = "T-Management"
    teachers_list = get_teacher_choice_tuple2(current_school)
    subject_list = get_subject_choice_tuple(current_school)
    school_teachers = get_teacher_objects(current_school)
    form = SubjectTeacherAllocationForm(subjects_tuple_list=subject_list, teachers_tuple_list=teachers_list)
    if request.method == "POST":
        form = SubjectTeacherAllocationForm(request.POST, subjects_tuple_list=subject_list, teachers_tuple_list=teachers_list)
        if form.is_valid():
            ct_allocated = form.cleaned_data["teacher_objs"]
            sb_allocated = form.cleaned_data["subjects_objs"]
            form.save()
            messages.success(
                request,
                _(f" {'Mr.' if ct_allocated.teacher_gender == 'M' else 'Ms.' } {ct_allocated.teacher_last_name} has been allocated {sb_allocated.subject_str_full} successfully🥳")
            )
            return redirect("schools:school_teacher_management_subject_allocation")
        else:
          context = {
            "form":form,
            "school":current_school,
            "page_title":page_title
          } 
    else:
        context = {
            "form":form,
            "school":current_school,
            "page_title":page_title,
            "teachers":school_teachers
        }
    return render(request, template_name, context)


#***--------------------***
#Student-school views
#***--------------------***
@verified_email_required
def student_registration(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/s_reg.html"
    page_title = "S-Registration"
    classes_list = current_school.school_classes_list
    form = StudentRegistrationForm(classes_tuple_list=classes_list)
    if classes_list:
        if request.method == "POST":
            form = StudentRegistrationForm(request.POST, request.FILES, classes_tuple_list=classes_list)
            if form.is_valid():
                form.save(student_school=current_school)     
                messages.success(
                    request,
                    f"student: {form.cleaned_data['student_first_name']} {form.cleaned_data['student_last_name']} saved successfully! 🥳"
                ) 
                return redirect(reverse("schools:school_student_registration"))
            else:
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form": form
            }
            return render(request, template_name, context)
    else:
        messages.warning(
            request,
            _(f"please create a class before adding students ⚠️")
        )
        context = {
            "school":current_school,
            "page_title":page_title,
            "form": form
        }
        return render(request, template_name, context)
    return render( request, template_name, context )

@verified_email_required
def student_enrollment(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/s_enroll.html"
    page_title = "S-Enrollment"
    classes_list = current_school.school_classes_list
    form = StudentEnrollmentForm(classes_tuple_list=classes_list)
    if request.method == "POST":
        form = StudentEnrollmentForm(request.POST,classes_tuple_list=classes_list)
        if form.is_valid():
            passed_first_name = form.cleaned_data["student_first_name"]
            passed_middle_name = form.cleaned_data["student_middle_name"]
            passed_last_name = form.cleaned_data["student_last_name"]
            passed_student_id = form.cleaned_data["student_id"]           
            passed_student_class = form.cleaned_data["student_class"]
            passed_student_dob = form.cleaned_data["student_dob"]
            try:
                enrolled_student = get_specific_student(passed_student_id)
                student_old_school = enrolled_student.student_school
                #check if passed values matter
                if enrolled_student.student_status != "T" and student_old_school != current_school:
                    messages.info(
                        request,
                        (f"Student {passed_last_name} : {passed_student_id} is yet to be released from {student_old_school.school_name} ")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form
                    }
                else:
                    #transfer the teacher to the new school
                    with transaction.atomic():
                        #internal update or external transfer
                        if student_old_school == current_school:
                            #data update or class transfer
                            if enrolled_student.student_class == passed_student_class:
                                enrolled_student.student_first_name = passed_first_name
                                enrolled_student.student_middle_name = passed_middle_name
                                enrolled_student.student_last_name = passed_last_name
                                enrolled_student.student_dob = passed_student_dob
                                enrolled_student.save(
                                    update_fields=[
                                        "student_first_name","student_middle_name","student_last_name","student_dob"
                                    ]
                                )
                                messages.success(
                                    request,
                                    (f"Student {passed_last_name} : {passed_student_id} records updated successfully")
                                )
                                context = {
                                    "school":current_school,
                                    "page_title":page_title,
                                    "form":StudentEnrollmentForm(classes_tuple_list=classes_list)
                                }
                            else:
                                #delete all past exams,reports for the class and create for the new ones
                                ResultsProfile.objects.filter(
                                    result_student=enrolled_student,
                                    result_class=enrolled_student.student_class
                                ).delete()
                                StudentEReportProfile.objects.filter(
                                    streport_student=enrolled_student,
                                    streport_class=enrolled_student.student_class
                                ).delete()
                                student_class_examinations = passed_student_class.examination_profiles.all()
                                student_class_subjects = passed_student_class.subject_profiles.all()
                                for examination in student_class_examinations:
                                    for subject in student_class_subjects:
                                        ResultsProfile.objects.create(
                                            result_student = enrolled_student,
                                            result_class = passed_student_class,
                                            result_school = passed_student_class.class_school,
                                            result_subject = subject,
                                            result_examination = examination
                                        )
                                    StudentEReportProfile.objects.create(
                                        streport_examination = examination,
                                        streport_class = passed_student_class,
                                        streport_student = enrolled_student,
                                    )                                                   
                                enrolled_student.student_first_name = passed_first_name
                                enrolled_student.student_middle_name = passed_middle_name
                                enrolled_student.student_last_name = passed_last_name
                                enrolled_student.student_dob = passed_student_dob
                                enrolled_student.student_class = passed_student_class
                                enrolled_student.save(
                                    update_fields=[
                                        "student_first_name","student_middle_name","student_last_name","student_dob",
                                        "student_class"
                                    ]
                                )
                                messages.success(
                                    request,
                                    (f"Student {passed_last_name} : {passed_student_id} transferred to {passed_student_class.class_full_str}")
                                )
                                context = {
                                    "school":current_school,
                                    "page_title":page_title,
                                    "form":StudentEnrollmentForm(classes_tuple_list=classes_list)
                                }
                        else:
                            enrolled_student.student_school = current_school
                            enrolled_student.student_status = "A"
                            # update the fields
                            enrolled_student.save(
                                update_fields=[
                                    "student_school","student_status"
                                ]
                            )
                            messages.success(
                                request,
                                (f"Student {passed_last_name} : {passed_student_id} enrolled successfully")
                            )
                            context = {
                                "school":current_school,
                                "page_title":page_title,
                                "form":StudentEnrollmentForm(classes_tuple_list=classes_list)
                            }
            except StudentProfile.DoesNotExist:
                messages.warning(
                    request,
                    (f"Student: {passed_last_name} {passed_student_id}:  Doesn't exist! Check your data!")
                )
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }
    return render(request, template_name, context)

@verified_email_required
def student_ledger_view(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/dashl1/school_index_students.html"
    page_title = "S-LedgerView"
    school_students = get_student_objects(current_school)
    form = StudentSearchForm()
    if request.method == "POST":
        if "st_ledger_search" in request.POST:
            form = StudentSearchForm(request.POST)
            if form.is_valid():
                search_value = form.cleaned_data["student_data"]
                student_search_results = get_searched_students(school_students,search_value)
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "school_students":school_students,
                    "form":form,
                    "search_results":student_search_results if student_search_results.exists() else "empty"
                }
            else:
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "school_students":school_students,
                    "form":form,
                    "search_results":None
                }
        elif "st_ledger_print" in request.POST:
            return student_ledger_generator(request)
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "school_students":school_students,
            "form":form,
            "search_results":None
        }
    return render(request, template_name, context)

@verified_email_required
def student_management(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    school_name = current_school.school_name
    template_name = "schools/usrmng/s_manage.html"
    page_title = "S-Management"
    if request.method == "POST":
        pass
    else:
        context = {
            "school":current_school,
            "school_name":school_name,
            "page_title":page_title,
        }
    return render(request, template_name, context)
#***--------------------***
#Parent-school views
#***--------------------***
@verified_email_required
def parent_registration(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
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
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:          
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }
    return render(request, template_name, context)
    
@verified_email_required
def parent_enrollment(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
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
                enrolled_parent = get_specific_parent(passed_parent_id)
                parent_first_name = enrolled_parent.parent_first_name
                parent_last_name = enrolled_parent.parent_last_name
                parent_gender = enrolled_parent.parent_gender
                parent_old_school = enrolled_parent.parent_school
                #check if passed values matter
                if parent_first_name == passed_first_name and parent_last_name == passed_last_name and parent_gender == passed_parent_gender :
                        #transfer the teacher to the new school
                    with transaction.atomic():
                        enrolled_parent.parent_school = current_school
                        #update the fields
                        enrolled_parent.save(
                            update_fields=[
                                "parent_school"
                            ]
                        )
                        messages.success(
                            request,
                            (f"Parent {parent_last_name} : {passed_parent_id} responsibility transferred from {parent_old_school.school_name} from {current_school.school_name} ")
                        )
                        context = {
                            "school":current_school,
                            "page_title":page_title,
                            "form":form
                        }
                else:
                    messages.warning(
                        request,
                        (f"Parent's data in inconsistent")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form
                    }
            except ParentProfile.DoesNotExist:
                messages.warning(
                    request,
                    (f"Parent: {passed_last_name} {passed_parent_id}:  Doesn't exist! Check your data!")
                )
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }
    return render(request, template_name, context)

@verified_email_required
def parent_management(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/p_manage.html"
    page_title = "P-Management"
    if request.method == "POST":
        pass
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
        }
    return render(request, template_name, context)
#***--------------------***
#NT-Staff-school views
#***--------------------***
@verified_email_required
def ntstaff_registration(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
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
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }
    return render(request, template_name, context)
    
@verified_email_required
def ntstaff_enrollment(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
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
                enrolled_ntstaff = get_specific_ntstaff(passed_ntstaff_id)
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
                            "school":current_school,
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
                            #update the fields
                            enrolled_ntstaff.save(
                                update_fields=[
                                    "ntstaff_school","ntstaff_h_qualification", "ntstaff_s_field", 
                                    "ntstaff_y_experience", "ntstaff_j_title"
                                ]
                            )
                            messages.success(
                                request,
                                (f"NTstaff {ntstaff_last_name} : {passed_ntstaff_id} enrolled successfully")
                            )
                            context = {
                                "school":current_school,
                                "page_title":page_title,
                                "form":form
                            }
                else:
                    messages.warning(
                        request,
                        (f"Ntstaff's data in inconsistent")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form
                    }
            except NtStaffProfile.DoesNotExist:
                messages.warning(
                    request,
                    (f"NTstaff: {passed_last_name} {passed_ntstaff_id}:  Doesn't exist! Check your data!")
                )
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form
                }
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form
        }

    return render(request, template_name, context)

@verified_email_required
def ntstaff_ledger_view(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/dashl1/school_index_ntstaff.html"
    page_title = "NT-LedgerView"
    school_ntstaffs = get_ntstaff_objects(current_school)
    school_scadmin_ntstaffs = get_filtered_ntstaff(school_ntstaffs,["SSCR","SBSR"])
    school_scsupport_ntstaffs = get_filtered_ntstaff(school_ntstaffs, ["SSOF","SOJT","SNSR"])
    school_stsupport_ntstaffs = get_filtered_ntstaff(school_ntstaffs, ["SLBT","SGOF"])
    school_ntstaffs_dict = {
        "scadmin_ntstaffs":set_filtered_ntstaff(school_scadmin_ntstaffs),
        "scsupport_ntstaffs":set_filtered_ntstaff(school_scsupport_ntstaffs),
        "scstsupport_ntstaffs":set_filtered_ntstaff(school_stsupport_ntstaffs)
    }
    form = NtStaffSearchForm()
    if request.method == "POST":
        form = NtStaffSearchForm(request.POST)
        if form.is_valid():
            search_value = form.cleaned_data["ntstaff_data"]
            ntstaff_search_results = get_searched_ntstaffs(school_ntstaffs,search_value)
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form,
                "search_results":ntstaff_search_results if ntstaff_search_results.exists() else "empty",
                "school_ntstaff_dict":school_ntstaffs_dict
            }
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form,
                "search_results":None,
                "school_ntstaff_dict":school_ntstaffs_dict
            }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form,
            "search_results":None,
            "school_ntstaff_dict":school_ntstaffs_dict
        }

    return render(request, template_name, context)

@verified_email_required
def ntstaff_management(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/usrmng/nt_manage.html"
    page_title = "NT-Management"
    if request.method == "POST":
        pass
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
        }
    return render(request, template_name, context)

#***--------------------***#***--------------------***
#Class-school views
#***--------------------***
@verified_email_required
def class_management(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/dashl0/school_classmng.html"
    page_title = "C-Management"
    school_classes = get_class_objects(current_school)
    school_classes_dict = {
        "north_classes":set_filtered_class(get_filtered_classes(school_classes, "N")),
        "south_classes":set_filtered_class(get_filtered_classes(school_classes, "S")),
        "east_classes":set_filtered_class(get_filtered_classes(school_classes, "E")),
        "west_classes":set_filtered_class(get_filtered_classes(school_classes, "W"))
    }
    teachers_list = get_teacher_choice_tuple2(current_school)
    form = ClassRegistrationForm(teachers_list=teachers_list)
    form2 = ClassDeletionForm()
    if teachers_list:
        if request.method == "POST":
            if  "class_registration" in request.POST:
                form = ClassRegistrationForm(request.POST, teachers_list=teachers_list)
                if form.is_valid():
                    response = form.save(current_school)
                    if response == 0 :
                        messages.success(
                            request,
                            f"The class was created successfully! 🥳"
                        )  
                    else:
                        messages.warning(
                            request,
                            f"The class already exists!"
                        )                    
                    return redirect(reverse("schools:school_class_management"))
                else:
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form,
                        "form2":form2,
                        "classes_dict":school_classes_dict
                    }
            elif  "class_deletion" in request.POST:
                form2 = ClassDeletionForm(request.POST)
                if form2.is_valid():
                    class_id = form2.cleaned_data["class_id"]
                    try: 
                        tobe_deleted_class = get_specific_class(class_id)
                        if tobe_deleted_class.class_school == current_school:
                            with transaction.atomic():
                                tobe_deleted_class.delete()
                                messages.success(
                                    request,
                                    _(f"Class {class_id} deleted successfully")
                                )
                                return redirect(reverse("schools:school_class_management"))
                        else:
                            messages.warning(
                                request,
                                (f"Can't delete a class you dont own")
                            )
                            context = {
                                "school":current_school,
                                "page_title":page_title,
                                "form":form,
                                "form2":form2,
                                "class_objs":school_classes_dict
                            }
                    except ClassProfile.DoesNotExist:
                        messages.warning(
                            request,
                            (f"class {class_id} Does not exist!")
                        )
                        context = {
                            "school":current_school,
                            "page_title":page_title,
                            "form":form,
                            "form2":form2,
                            "classes_dict":school_classes_dict
                        }
                else:
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form,
                        "form2":form2,
                        "classes_dict":school_classes_dict
                    }
            else:
                print("An unidentified form recieved")  
                return redirect(reverse("schools:school_class_management"))          
        else:
            context = {
                "school":current_school,
                "page_title":page_title,
                "form":form,
                "form2":form2,
                "classes_dict":school_classes_dict
            }
    else:
        messages.warning(
            request,
            f"please create a teacher first ⚠️"
        ) 
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form,
            "form2":form2,
            "classes_dict":school_classes_dict
        }   
    return render(request, template_name, context)

#***--------------------***#***--------------------***
#Assessments-school views
#***--------------------***
@verified_email_required
def assessment_management(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/dashl0/school_assess.html"
    page_title = "A-Management"
    classes_list = current_school.school_classes_list
    school_results = current_school.school_result_objects
    form = SchoolLocksForm()
    form2 = ResultsFilterForm(classes_tuple_list=classes_list)
    if request.method == "POST":
        if "get_results" in request.POST:
            form2 = ResultsFilterForm(request.POST, request.FILES, classes_tuple_list=classes_list)
            if form2.is_valid():
                formfields = ["result_class", "result_term", "result_period", "result_year", "result_options"]
                formdata = { field : form2.cleaned_data[f"{field}"] for field in formfields}
                try:
                    examination_q = ExaminationProfile.objects.get(
                        examination_class = formdata["result_class"],
                        examination_term = formdata["result_term"],
                        examination_period = formdata["result_period"],
                        examination_year = formdata["result_year"]
                    )
                except ExaminationProfile.DoesNotExist:
                    messages.warning(
                        request,
                        _("No examination profile found for the selected class, term, period and year.")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form,
                        "form2":form2
                    }
                    return render(request, template_name, context)
                except ExaminationProfile.MultipleObjectsReturned:
                    messages.warning(
                        request,
                        _("System error: multiple matching examination profiles found. Contact support.")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form,
                        "form2":form2
                    }
                    return render(request, template_name, context)
                #generate reports total and position
                try:
                    obj = formdata["result_class"]
                    obj.class_reports_total_generator(examination_q)
                    obj.class_reports_pos_generator(examination_q)
                except (ValidationError, ObjectDoesNotExist, ValueError, TypeError) as e:
                    messages.warning(
                        request,
                        _(f"Error ({e}): preventing automatic report generation")
                    )
                    context = {
                        "school":current_school,
                        "page_title":page_title,
                        "form":form,
                        "form2":form2
                    }
                    return render(request, template_name, context)
                #print the reports if method is print
                if formdata["result_options"] == str(1):
                    return student_report1_generator(class_passed=formdata["result_class"], exam_passed=examination_q)
                class_students = (
                    formdata["result_class"]
                    .student_profiles.all()
                    .annotate(
                        total_score=Subquery(
                            StudentEReportProfile.objects.filter(
                                streport_student=OuterRef('pk'),
                                streport_examination=examination_q,
                            )
                            .values('streport_t_score')[:1]
                        )
                    )
                    .order_by('-total_score', 'student_first_name')
                )
                results_qs = (
                    ResultsProfile.objects.filter(
                        result_examination=examination_q,
                        result_student__in=class_students,
                    )
                    .select_related('result_subject', 'result_student')
                    .order_by('result_subject__subject_name')
                )
                ereport_qs = StudentEReportProfile.objects.filter(
                    streport_examination = examination_q,
                    streport_student__in = class_students
                )
                class_students = class_students.prefetch_related(
                    Prefetch('result_profiles', queryset=results_qs, to_attr='prefetched_results'),
                    Prefetch('stereport_profile', queryset=ereport_qs, to_attr='prefetched_ereport'),
                )
                students_results_dict = {
                    student : (
                        student.prefetched_results,
                        student.prefetched_ereport[0] if student.prefetched_ereport else None
                    ) for student in class_students
                }
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form2":form2,
                    "class_fetched":formdata["result_class"],
                    "class_students":class_students,
                    "students_results_dict":students_results_dict
                }
            else:
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form,
                    "form2":form2
                }
        elif "manage_results" in request.POST:
            form = SchoolLocksForm(request.POST)
            if form.is_valid():
                school_rupload_lock = form.cleaned_data["school_rupload_lock"]
                school_reportgen_lock = form.cleaned_data["school_reportgen_lock"]
                current_school.school_rupload_lock = school_rupload_lock
                current_school.school_reportgen_lock = school_reportgen_lock
                current_school.save(update_fields=["school_rupload_lock","school_reportgen_lock"])
                return redirect("schools:school_assessment_management")
            else:
                context = {
                    "school":current_school,
                    "page_title":page_title,
                    "form":form,
                    "form2":ResultsFilterForm(classes_tuple_list=classes_list)
                }
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
            "form":form,
            "form2":form2
        }
    return render(request, template_name, context)

#***--------------------***#***--------------------***
#Settings views
#***--------------------***
@verified_email_required
def school_settings(request):
    if request.user.user_type != "school":
        return HttpResponse("Only schools allowed bro!")
    if school_uuid != valid_school_uuid:
        return HttpResponse("Wrong school trying to access the page")
    current_school = get_school_object(request.user)
    template_name = "schools/dashl0/school_classmng.html"
    page_title = "S-Settings"
    if request.method == "POST":
        pass
    else:
        context = {
            "school":current_school,
            "page_title":page_title,
        }

    return render(request, template_name, context)