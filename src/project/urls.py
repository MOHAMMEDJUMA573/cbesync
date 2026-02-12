from django.contrib import admin
from django.urls import path, include
from . import views


#can use logging to log any ip to admins path
urlpatterns = [
    path('admincbesync/', admin.site.urls),
    #project urls
    path('',views.homepage, name="main_app_home"),
    #apps urls
    path('school/', include("schools.urls")),
    path('teacher/', include("teachers.urls")),
    #allauth urls
    path('accounts/', include('allauth.urls')),
]
