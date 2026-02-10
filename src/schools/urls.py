from django.urls import path, include
from . import views

#namespace the app
app_name = "schools"

#main urls
#can use logging to log any ip to admins path
urlpatterns = [
    path("",views.dashboard, name="school_app_dashboard"),
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
                path("teacher_enrl/", views.teacher_enrollment, name="school_teacher_enrollment"),
                path("student_enrl/", views.student_enrollment, name="school_student_enrollment"),
                path("parent_enrl/", views.parent_enrollment, name="school_parent_enrollment"),
                path("ntstaff_enrl/", views.ntstaff_enrollment, name="school_ntstaff_enrollment"),
                path("teacher_mng/", views.teacher_management, name="school_teacher_management"),
                path("student_mng/", views.student_management, name="school_student_management"),
                path("parent_mng/", views.parent_management, name="school_parent_management"),
                path("ntstaff_mng/", views.ntstaff_management, name="school_ntstaff_management"),
                
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
    ),
    path(
        "class_management/",
        include(
            [
                path("", views.class_management, name="school_class_management")
            ]
        )
    ),
    path(
        "assessment_management/",
        include(
            [
                path("", views.assessment_management, name="school_assessment_management")
            ]
        )
    )
]
