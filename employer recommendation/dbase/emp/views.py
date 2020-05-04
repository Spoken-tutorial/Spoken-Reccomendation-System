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

def roles(request):
    return render(request,'emp/role.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('student')
    return render(request,'emp/main_index.html')
# student section
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

# company sections
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

def results(request):
    alljobs=jobs.objects.all()
    context={'alljobs':alljobs}
    #print(alljobs)
    #if request.method=='POST':

    return render( request,'emp/results.html',context)



#o(n^2) algo for recommending
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

# only students
def studentpg(request):
    #p=appliedjobs.objects.all()

    return render(request,'emp/student_section.html')

# only students

@allowed_users(allowed_roles=['students'])                 #for student profile
def profile(request):
    student=request.user.student
    form=studentform(instance=student)

    if request.method =='POST':
        form=studentform(request.POST, request.FILES,instance=student)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'emp/student_profile.html',context)



def student_page(request):

    return render(request,'emp/sindex.html')


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
@allowed_users(allowed_roles=['employer'])
def company(request):
    name=request.user.employer.jobs_set.all()
    #name=request.user.employer.
    #print(name)
    context={'name':name}
    return render(request,'emp/employer_section.html',context)

#logout
def handlelogout(request):

    logout(request)
    return redirect('index')
    return HttpResponse('404 Not found')

# sign up page

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
    # temporary login page

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        if request.method=='POST':

            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.info(request,'username or password is incorrect')

        return render(request, 'emp/login.html')

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

def delete_job(request,pk):
    jb = jobs.objects.get(id=pk)
    if request.method=='POST':
        jb.delete()
        return redirect('employer')
    context={'item':jb}
    return render(request,'emp/delete_job.html',context)