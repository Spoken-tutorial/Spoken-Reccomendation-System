from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request,"company/index_c.html")
    #return HttpResponse("hello")
def postjob(request):
    return HttpResponse("we are at postjob")