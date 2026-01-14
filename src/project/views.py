from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_not_required


@login_not_required
def homepage(request):
   #use http response e.g when the user in not appropriate
   context = {
      
   }

   return render(request, "project/index.html", context)