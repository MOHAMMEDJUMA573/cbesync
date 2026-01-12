from django.http import HttpResponse
import uuid

valid_school_uuid = uuid.UUID("075194d3-6885-417e-a8a8-6c931e272f01")


def dashboard(request, school_uuid):
    if school_uuid == valid_school_uuid:
        return HttpResponse(f"<h1>Right guy {school_uuid}</h1>")
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid}</h1>")

def user_management(request, school_uuid):
    if school_uuid == valid_school_uuid:
        return HttpResponse(f"<h1>Right guy {school_uuid} user management page</h1>")
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} user management page</h1>")

def class_management(request, school_uuid):
    if school_uuid == valid_school_uuid:
        return HttpResponse(f"<h1>Right guy {school_uuid} class management</h1>")
    else:
        return HttpResponse(f"<h1>Wrong guy {school_uuid} class management</h1>")
