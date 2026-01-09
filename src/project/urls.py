from django.contrib import admin
from django.urls import path

#can use logging to log any ip to admins path
urlpatterns = [
    path('admin/', admin.site.urls),
]
