from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_not_required


@login_not_required
def homepage(request):

   if request.user.is_authenticated:
      print("authenticated")
      if request.user.user_type == "school":
         return redirect("schools:school_app_dashboard")
      elif request.user.user_type == "teacher":
         return redirect("teachers:teacher_app_dashboard")
   #use http response e.g when the user in not appropriate
   context = {
      
   }

   return render(request, "project/index.html", context)