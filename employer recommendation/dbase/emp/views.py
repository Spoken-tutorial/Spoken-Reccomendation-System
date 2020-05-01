from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponse, redirect
from .models import student, employer, jobs, appliedjobs
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .decorators import unauthenticated_user, allowed_users, employers_only
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib.auth.models import Group


def index(request):
    if request.user.is_authenticated:
        return redirect('student')
    return render(request, 'emp/main_index.html')


# student section
def apply(request):
    if request.method == 'POST':
        name = request.POST['name']
        skills = request.POST['skills']
        share = request.POST['share']
        print(name, skills, share)

        if len(name) < 2 or len(skills) == 0:
            messages.error(request, "Please fill it correctly")
        else:
            stud = student(name=name, skills=skills, experience=share)
            stud.save()
            messages.success(request, "Profile has been updated")
    return render(request, 'emp/apply.html')


# company sections
def post(request):
    messages.success(request, 'This is employers section')
    if request.method == 'POST':
        name = request.POST['name']
        title = request.POST['title']
        location = request.POST['location']
        skills = request.POST['skills']
        share = request.POST['share']
        cmp = employer(company_name=name)
        cmp.save()

        jb = jobs(jobtitle=title, joblocation=location, jobskills=skills, jobdescription=share, employer=cmp)
        jb.save()
    return render(request, 'emp/post.html')


def results(request):
    alljobs = jobs.objects.all()
    context = {'alljobs': alljobs}
    # print(alljobs)
    # if request.method=='POST':

    return render(request, 'emp/results.html', context)


# o(n^2) algo for recommending
def recommend(request):
    alljobs = jobs.objects.all()
    stud = student.objects.all()
    for job in alljobs:
        for st in stud:
            dj = job.jobskills.split(',')
            ds = st.skills.split(',')
            for s in ds:
                if s in dj:
                    print(job.jobtitle, st.name)

    return render(request, 'emp/recommend.html')


# login
def signin(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        if request.method == 'POST':
            # get post parameters
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # message
                return redirect('student')
            else:
                # message
                messages.info(request, 'username or password is incorrect')
        return render(request, 'emp/login.html')


@login_required(login_url='login')
@employers_only
@allowed_users(allowed_roles=['students'])
# only students
def student(request):
    p = appliedjobs.objects.all()
    name = request.user.student.name

    print(p)
    return render(request, 'emp/student_section.html')


# only students
@login_required(login_url='login')
@allowed_users(allowed_roles=['students'])
def student_profile(request):
    # work in progress
    name = request.user.student.jobs.all()
    print(name)


# decorators to allow only employer
@allowed_users(allowed_roles=['employer'])
def company(request):
    return render(request, 'emp/employer_section.html')


# logout
def handlelogout(request):
    logout(request)
    return redirect('index')
    return HttpResponse('404 Not found')


# sign up page

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='students')
                user.groups.add(group)
                messages.success(request, 'Account was created for ' + username)
                return redirect("login")
        context = {'form': form}
        return render(request, 'emp/reg.html', context)

    # temporary login page


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('student')
    else:
        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'emp/login.html')

