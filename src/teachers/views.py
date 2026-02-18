from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from allauth.account.decorators import verified_email_required
from django.utils.translation import gettext_lazy as _
import uuid
from classes.models import ClassProfile
from subjects.models import SubjectProfile
from students.models import StudentProfile
from results.forms import TeacherResultsUploadForm

valid_teacher_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
teacher_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#functions to get items
def get_teacher_object(user_passed):
    return user_passed.teacher_profile

#***--------------------***#***--------------------***
#Dashboard-teacher views
#***--------------------***
@verified_email_required
def dashboard(request):
    if request.user.user_type == "teacher":
        current_teacher = get_teacher_object(request.user)
        teacher_school = current_teacher.teacher_school
        if teacher_uuid == valid_teacher_uuid:
            template_name = "teachers/dashl0/teacher_index.html"
            page_title = "T-Dashboard"
            context = {
                "page_title":page_title,
                "teacher":current_teacher,
                "teacher_school":teacher_school
            }
        else:
            return HttpResponse("Wrong teacher trying to access the page!")
    else:
        return HttpResponse("Only teachers allowed bro!")
    return render(request, template_name, context)

#***--------------------***#***--------------------***
#   Teacher-classes views
#***--------------------***
@verified_email_required
def class_teacher_classes(request):
    if request.user.user_type == "teacher":
        current_teacher = get_teacher_object(request.user)
        teacher_school = current_teacher.teacher_school
        teacher_classes = ClassProfile.objects.filter(class_teacher=current_teacher)
        if teacher_uuid == valid_teacher_uuid:
            template_name = "teachers/dashl0/teacher_class.html"
            page_title = "T-Classes"
            context = {
                "page_title":page_title,
                "teacher":current_teacher,
                "teacher_school":teacher_school,
                "teacher_classes":teacher_classes,
            }
        else:
            return HttpResponse("Wrong teacher trying to access the page!")
    else:
        return HttpResponse("Only teachers allowed bro!")
    return render(request, template_name, context)
#***--------------------***#***--------------------***
#   Teacher-subject result upload views
#***--------------------***
@verified_email_required
def teacher_classes_results_upload(request):
    if request.user.user_type == "teacher":
        current_teacher = get_teacher_object(request.user)
        teacher_school = current_teacher.teacher_school
        teacher_subjects = current_teacher.teacher_teaching_subjects
        #form inits
        teacher_classes_set = set()
        for subject in teacher_subjects:
            teacher_classes_set.add(subject.subject_class)

        subjects_tuple_list = [
            (str(c.subject_id), str(f"{c.subject_name} --- {c.subject_class.class_full_str}"))
            for c in teacher_subjects
        ]
        form = TeacherResultsUploadForm(subjects_tuple_choices=subjects_tuple_list)
        if teacher_uuid == valid_teacher_uuid:
            template_name = "teachers/dashl0/teacher_rupload.html"
            page_title = "R-uploads"
            if request.method == "POST":
                form = TeacherResultsUploadForm(request.POST,subjects_tuple_choices=subjects_tuple_list)
                if form.is_valid():
                    passed_subject = form.cleaned_data["results_subjects"]
                    passed_subject_class = passed_subject.subject_class
                    passed_subject_students = passed_subject_class.student_profiles.all()
                    print(passed_subject_students)
                    return HttpResponse(f"{passed_subject_students}")
                else:
                    context = {
                    "page_title":page_title,
                    "teacher":current_teacher,
                    "teacher_school":teacher_school,
                    "teacher_subjects":teacher_subjects,
                    "form":form,
                }
            else:
                context = {
                "page_title":page_title,
                "teacher":current_teacher,
                "teacher_school":teacher_school,
                "teacher_subjects":teacher_subjects,
                "form":form,
            }
        else:
            return HttpResponse("Wrong teacher trying to access the page!")
    else:
        return HttpResponse("Only schools allowed bro!")
    return render(request, template_name, context)