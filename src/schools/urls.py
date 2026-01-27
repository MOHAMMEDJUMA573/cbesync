from django.urls import path, include
from . import views

#namespace the app
app_name = "schools"

#main urls
#can use logging to log any ip to admins path
urlpatterns = [
    path("",views.dashboard, name="school_app_dashboard"),
    path("class_management/",views.class_management, name="school_cls_management"),
]
#secondary urls patterns
urlpatterns+=[
    path(
        "user_management/",
        include(
            [
                path("", views.user_management, name="school_usr_management"),
                path("teacher_reg/", views.teacher_registration, name="school_teacher_registration"),
                path("student_reg/", views.student_registration, name="school_student_registration"),
                path("parent_reg/", views.parent_registration, name="school_parent_registration"),
                path("ntstaff_reg/", views.ntstaff_registration, name="school_ntstaff_registration"),
            ]
        ),
    ),
    path(
        "ledger_view/",
        include(
            [
                path("students/", views.student_ledger_view, name="school_student_ledgerview"),
                path("teachers/", views.teacher_ledger_view, name="school_teacher_ledgerview"),
                path("ntstaffs/", views.ntstaff_ledger_view, name="school_ntstaff_ledgerview"),
            ]
        )
    )
]
