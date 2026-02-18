from django.urls import path, include
from . import views

#namespace the app
app_name = "teachers"

urlpatterns = [
    path("",views.dashboard, name="teacher_app_dashboard"),
]

#secondary urls patterns
urlpatterns+=[
    path(
        "myclasses/",
        include(
            [
                path("", views.class_teacher_classes, name="teacher_classes_management"),
            ]
        ),
    ),
    path(
        "r-uploads/",
        include(
            [
                path("", views.teacher_classes_results_upload_redirect, name="teacher_classes_rupload"),
                path("<class_id>/<uuid:subject_id>/<uuid:exam_id>/", views.teacher_classes_results_upload_subject, name="teacher_classes_rupload_subject")
            ]
        )
    ),
    path(
        "subjects/",
        include(
            []
        )
    ),
    path(
        "resources/",
        include(
            []
        )
    ),
    path(
        "profile/",
        include(
            []
        )
    ),
    path(
        "reports/",
        include(
            []
        )
    ),
    path(
        "settings/",
        include(
            []
        )
    )
]
