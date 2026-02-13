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
        "uploads/",
        include(
            []
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
