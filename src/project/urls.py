from django.contrib import admin
from django.urls import path, include
from . import views


#can use logging to log any ip to admins path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage, name="main_app_home"),
    path('school/', include("schools.urls")),
    #allauth urls
    path('accounts/', include('allauth.urls')),
]
