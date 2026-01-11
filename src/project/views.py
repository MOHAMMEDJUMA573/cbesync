from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
   #use http response e.g when the user in not appropriate
   context = {
      
   }

   return render(request, "project/index.html", context)