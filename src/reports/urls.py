from django.urls import path, include
from . import views

#namespace the app
app_name = "reports"

urlpatterns = [
    path("", views.student_report1_generator, name="class_report_genlink"),
]

#secondary urls patterns
urlpatterns+=[]
