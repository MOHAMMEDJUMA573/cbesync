from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from allauth.account.decorators import verified_email_required
from django.utils.translation import gettext_lazy as _
import uuid
from classes.models import ClassProfile
from results.models import SubjectProfile
from teachers.models import TeacherProfile

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
        t_classes_array = [
            (c, SubjectProfile.objects.filter(subject_class=c.id).count(), SubjectProfile.objects.filter(subject_class=c.id))
            for c in ClassProfile.objects.filter(class_teacher=current_teacher)
        ]
        subject_t_dict = {}
        class_s_teacher_count = []
        for item in t_classes_array:
            # print(item[0],"\n\countn\n", item[1] ,"\nsubjects\n", item[2])
            for subject in item[2]:
                subject_teacher = subject.subject_teacher
                if subject_teacher:
                    if subject_t_dict.get(subject_teacher):
                        subject_t_dict[subject_teacher] += [subject]
                    else:
                        subject_t_dict.update({subject_teacher: [subject]})
        print(subject_t_dict)
            
        if teacher_uuid == valid_teacher_uuid:
            template_name = "teachers/dashl0/teacher_class.html"
            page_title = "T-Classes"
            context = {
                "page_title":page_title,
                "teacher":current_teacher,
                "teacher_school":teacher_school,
                "teacher_classes":t_classes_array
            }
        else:
            return HttpResponse("Wrong teacher trying to access the page!")
    else:
        return HttpResponse("Only teachers allowed bro!")
    return render(request, template_name, context)
