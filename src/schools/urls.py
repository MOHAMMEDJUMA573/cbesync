from django.urls import path, include
from . import views

#namespace the app
app_name = "schools"

#main urls
#can use logging to log any ip to admins path
urlpatterns = [
    path("",views.dashboard, name="school_app_dashboard"),
    path("user_management/",views.user_management, name="school_usr_management"),
    path("class_management/",views.class_management, name="school_cls_management"),
]
#secondary urls patterns
urlpatterns+=[
    path(
        "user_management/",
        include(
            [
                path("teacher_reg/", views.teacher_registration, name="school_teacher_registration"),
            ]
        ),
    ),
]
