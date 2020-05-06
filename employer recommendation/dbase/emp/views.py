from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,HttpResponse,redirect
from .models import student,employer,jobs,appliedjobs
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from .decorators import unauthenticated_user,allowed_users,employers_only
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,studentform,companyform,postjobform
from django.contrib.auth.models import Group
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template
import datetime

# function for retrieving students profile
def forstu(request):
    name = request.user.student.name
    education = request.user.student.education
    exp = request.user.student.experience
    mail = request.user.student.mail
    skills = request.user.student.skills
    about = request.user.student.about
    git = request.user.student.github
    lnk = request.user.student.Linkedin
    ph = request.user.student.phno
    tscore = request.user.student.Spokentest_score
    gpa = request.user.student.gpa
    lst = skills.split(",")
    stream = request.user.student.degree
    startyear = request.user.student.startyear
    endyear = request.user.student.endyear
    address = request.user.student.address
    upload_your_work=request.user.student.upload_your_work
    data = {'name': name, 'lnk': lnk, 'gpa': gpa, 'education': education, 'tscore': tscore, 'exp': exp, 'mail': mail,
            'skills': lst, 'about': about, 'git': git, 'address': address, 'ph': ph, 'startyear': startyear,
            'endyear': endyear, 'stream': stream}
    context = {'data': data}

    return context

#--------------------------------               Main Page
def index(request):
    if request.user.is_authenticated:
        return redirect('student')
    return render(request,'emp/main_index.html')


# student section





# company sections
#----------------------------------Post Job details
@login_required(login_url='login')
def postjob(request):

    if request.method=='POST':
        #name=request.POST['name']
        title=request.POST['title']
        location=request.POST['location']
        skills=request.POST['skills']
        share=request.POST['share']
        cate=request.POST['cate']
        criteria=request.POST['criteria']
        cmp=request.user.employer
        #cmp.save()

        jb=jobs(jobtitle=title,joblocation=location,jobskills=skills,jobdescription=share,jobcategory=cate,criteria=criteria,employer=cmp)
        jb.save()
        return redirect('employer')
    return render(request,'emp/postjob.html')



# ---------------------------------for generating Student report in Pdf format
# students section
@login_required(login_url='login')
@allowed_users(allowed_roles=['students'])

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        context=forstu(request)

        pdf = render_to_pdf('emp/pdf_student.html',context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")




# ----------------------just a basic attempt o(n^2) algo for recommending  will work later

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


# login
def signin(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        if request.method == 'POST':
         # get post parameters
            username=request.POST['username']
            password=request.POST['password']

            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
            #message
                return redirect('student')
            else:
           #message
                messages.info(request, 'username or password is incorrect')
        return render(request,'emp/login.html')



@login_required(login_url='login')
@employers_only
@allowed_users(allowed_roles=['students'])

# only for students.....-----------------------Student main dashboard


def studentpg(request):

    if request.user.student.name==" ":
        return render(request, 'emp/student_section.html')
    else:

        a1 = appliedjobs.objects.filter(student__name__startswith=request.user.student)
        if len(a1)==1:

            date = a1[0].date_created
        # print(a1.student.all())

            data = a1[0].jobs.all()
            context = {'data': data, 'date': date}

            return render(request,'emp/student_section.html',context)


    return render(request, 'emp/student_section.html')

# only students
#----------------------------------------------for student profile settings


@allowed_users(allowed_roles=['students'])
def student_profile(request):
    student=request.user.student
    form=studentform(instance=student)

    if request.method =='POST':
        form=studentform(request.POST, request.FILES,instance=student)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'emp/student_profile.html',context)

#-----------------------------------------------student profile card


@allowed_users(allowed_roles=['students'])
def student_page(request):
    context=forstu(request)
    return render(request,'emp/sindex.html',context)

#--------------------------------------employer profile settings part


@allowed_users(allowed_roles=['employer'])
def employer_profile(request):
    company=request.user.employer
    form=companyform(instance=company)

    if request.method=='POST':
        form=companyform(request.POST,request.FILES,instance=company)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'emp/employer_profile.html',context)





# decorators to allow only employer
#-------------------------------------Company dashboard for deleting and updating posted jobs


@allowed_users(allowed_roles=['employer'])
def company(request):
    name=request.user.employer.jobs_set.all()
    details=request.user.employer
    context={'name':name,'details':details}
    return render(request,'emp/employer_section.html',context)

#----------------------------------------------logout

def handlelogout(request):

    logout(request)
    return redirect('index')
    return HttpResponse('404 Not found')

#------------------------------------- sign up page for student

def registerpage_student(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        form=CreateUserForm()

        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username=form.cleaned_data.get('username')
                group=Group.objects.get(name='students')
                user.groups.add(group)
                student.objects.create(user=user,)
                messages.success(request,'Account was created for '+ username)
                return redirect("login")
        context={'form':form}
        return render(request,'emp/reg.html',context)


#--------------------------------------------sign up page for employer


def registerpage_employer(request):
    if request.user.is_authenticated:
        return redirect('employer')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group=Group.objects.get(name='employer')
                user.groups.add(group)
                employer.objects.create(user=user,)
                messages.success(request, 'Account was created for ' + username)
                return redirect("login")
        context = {'form': form}
        return render(request, 'emp/reg.html', context)



# ----------------------------create job
# for employers only

@allowed_users(allowed_roles=['employer'])
def create_job(request):
    form=postjobform()
    if request.method=='POST':
        print(request.POST)
        form=postjobform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employer')
    context={'form':form}

    return render(request,'emp/createjob.html',context)


#!-------------------------------------------------udate job details
#-------------------------- for employers

@allowed_users(allowed_roles=['employer'])
def update_job(request,pk):
    jb=jobs.objects.get(id=pk)
    form=postjobform(instance=jb)

    if request.method=='POST':
        #print(request.POST)
        form=postjobform(request.POST,instance=jb)
        if form.is_valid():
            form.save()
            return redirect('employer')
    context={'form':form}


    return render(request,'emp/createjob.html',context)

#!-------------------------------------------------Delete job details
#-------------------------- for employers


@allowed_users(allowed_roles=['employer'])
def delete_job(request,pk):
    jb = jobs.objects.get(id=pk)
    if request.method=='POST':
        jb.delete()
        return redirect('employer')
    context={'item':jb}
    return render(request,'emp/delete_job.html',context)


# for students to search job

@allowed_users(allowed_roles=['students'])
def searchjob(request):
    query=request.GET.get('search')
    head=[]
    titlejobs=jobs.objects.values('jobtitle','id')      #list of dict

    title={item['jobtitle'] for item in titlejobs}
    lst=list(title) # set of job titles
    print(lst)

    titletemp=jobs.objects.filter(jobtitle=query)

    head=titletemp
    if query in lst:
        context={'head':head}

        return render(request,'emp/searchjob.html',context)
    else:
        return HttpResponse("no item found.Search for job title like Django developer , Java developer")


#!------------------------------showcasing all jobs to students posted by companies no filtering initially.will apply later
# for students

@allowed_users(allowed_roles=['students'])
def apply_jobs(request):
    if request.user.student.name==" ":
        return redirect('profile')
    else:
        job=jobs.objects.all()
        s1=request.user.student

        total=len(job)
        #print(job)
        context={'job':job}

        return render(request,'emp/apply.html',context)
    return HttpResponse("404 NOT FOUND")

# for students
#  student will apply for jobs
# used appliedjobs models to access (many to many field)
@allowed_users(allowed_roles=['students'])


def jobs_applied(request,pk):
    application=appliedjobs.objects.all()
    st=request.user.student                          #student object
    jb = jobs.objects.get(id=pk)                     # job object
    #print(jb.jobskills)
    a1=appliedjobs.objects.filter(student__name__startswith=request.user.student)                                #applied objects
    if len(a1)==1:
        a1[0].jobs.add(jb)
        print(a1)
        a1[0].save()
        date=a1[0].date_created
    #print(a1.student.all())

        data=a1[0].jobs.all()
        context={'data':data,'date':date}
        return render(request,'emp/student_section.html',context)
    else:
        a1=appliedjobs()
        a1.save()
        a1.jobs.add(jb)
        a1.student.add(st)

        data = a1.jobs.all()
        date = a1.date_created
        context = {'data': data, 'date': date}
        return render(request, 'emp/student_section.html', context)

    #print(application[1].student.all())  student object
    #print(application[1].jobs.all())         jobs applied object
    p=application[1].jobs.all()

    return HttpResponse("404 not found")






