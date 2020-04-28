from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,"student/index_s.html")

def apply(request):
    return HttpResponse("Apply page")