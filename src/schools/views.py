from django.http import HttpResponse
from django.shortcuts import render
import uuid

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")
school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")

#man_dashbordand subs
def dashboard(request):
    if school_uuid == valid_school_uuid:
        template_name = "schools/dashl0/school_index.html"
        page_title = "Dashboard"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user dashbord page</h1>")
    
    return render(request, template_name, context)

#usermanagement and subs
def user_management(request):
    if school_uuid == valid_school_uuid:
        template_name = "schools/dashl0/school_usermng.html"
        page_title = "Management"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user management page</h1>")
    
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

def student_registration(request):
    if school_uuid == valid_school_uuid:
        template_name = "schools/usrmng/s_reg.html"
        page_title = "S-Management"

        context = {
            "page_title":page_title
        }
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user management page</h1>")
    
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
#class management and subs
def class_management(request):
    if school_uuid == valid_school_uuid:
        return HttpResponse(f"<h1>Right guy {school_uuid} class management</h1>")
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} class management</h1>")
