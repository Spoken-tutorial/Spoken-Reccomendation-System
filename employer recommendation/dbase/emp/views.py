from django.shortcuts import render,HttpResponse,redirect
from .models import student,employer,jobs
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def index(request):
    return render(request,'emp/main_index.html')
def apply(request):

    if request.method =='POST':
        name = request.POST['name']
        skills = request.POST['skills']
        share= request.POST['share']
        print(name,skills,share)

        if len(name)<2 or len(skills)==0:
            messages.error(request,"Please fill it correctly")
        else:
            stud = student(name=name, skills=skills, experience=share)
            stud.save()
            messages.success(request,"Profile has been updated")
    return render(request,'emp/apply.html')
def post(request):
    messages.success(request, 'This is employers section')
    if request.method=='POST':
        name=request.POST['name']
        title=request.POST['title']
        location=request.POST['location']
        skills=request.POST['skills']
        share=request.POST['share']
        cmp=employer(company_name=name)
        cmp.save()

        jb=jobs(jobtitle=title,joblocation=location,jobskills=skills,jobdescription=share,employer=cmp)
        jb.save()
    return render(request,'emp/post.html')

def results(request):
    alljobs=jobs.objects.all()
    context={'alljobs':alljobs}
    #print(alljobs)
    #if request.method=='POST':

    return render( request,'emp/results.html',context)
def recommend(request):
    alljobs=jobs.objects.all()
    stud=student.objects.all()
    for job in alljobs:
        for st in stud:
            dj=job.jobskills.split(',')
            ds=st.skills.split(',')
            for s in ds:
                if s in dj:
                    print(job.jobtitle,st.name)

    return render(request,'emp/recommend.html')

def signup(request):

    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1!=password2:
            return redirect('index')
        myuser = User.objects.create_user(username, email, password1)
        myuser.save()
        return redirect('login')


    else:

        return render(request,'emp/signup.html')


def signin(request):
    if request.method == 'POST':
     # get post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
        #message
            return redirect('student')
        else:
       #message
            return redirect('index')
    return render(request,'emp/login.html')


def student(request):
    return render(request,'emp/student_section.html')
def company(request):
    return render(request,'emp/employer_section.html')


def handlelogout(request):

    logout(request)
    return redirect('index')
    return HttpResponse('404 Not found')
