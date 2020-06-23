from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,HttpResponse,redirect
from .models import student,employer,jobs,appliedjobs,Contact,contact_stu,rate,student_status,Post,blogcomment,pay,payUpdate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from .decorators import unauthenticated_user,allowed_users,employers_only
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,studentform,companyform,postjobform     # forms
from django.contrib.auth.models import Group
from django.views.generic import View
from .utils import render_to_pdf                                       # making pdf
from django.template.loader import get_template
import datetime
from django.core.mail import send_mail                                   # mail sending
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum                                               # payment configuration

# function for retrieving students profile
# students information
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

    data = {'name': name, 'lnk': lnk, 'gpa': gpa, 'education': education, 'tscore': tscore, 'exp': exp, 'mail': mail,
            'skills': lst, 'about': about, 'git': git, 'address': address, 'ph': ph, 'startyear': startyear,
            'endyear': endyear, 'stream': stream}
    context = {'data': data}

    return context

#--------------------------------               Main Page
def index(request):
    if request.user.is_authenticated:
        return redirect('student')
    jb=jobs.objects.all()
    print(jb)

    jb1=jb[:3]
    print(jb1)
    #head1=jb1
    head2=jb[:5]

    jo=len(jb)
    jb.reverse()
    head1=jb[(jo-3):]
    print(jb[jo-1])
    js=student.objects.all()
    j1=len(js)
    emplo=employer.objects.all()
    emplo1=len(emplo)
    if request.method =='POST':

        email=request.POST['email_user']
        comment=request.POST['comment_user']
        con=Contact(email=email,comment=comment)
        con.save()
        send_mail('Spoken Recommendation', 'Thank You for contacting us! we will reach to you soon'
                  , settings.EMAIL_HOST_USER,
                  [email],fail_silently=False
                  )
        messages.success(request,'Thank you! We will reach you soon ')
    r=rate.objects.all()
    lst_rating=[]
    for i in r:
        lst_rating.append(i.rating)                                                         # user rating graph
    lt=len(lst_rating)
    sr1=lst_rating.count(1)
    sr2=lst_rating.count(2)
    sr3=lst_rating.count(3)
    sr4=lst_rating.count(4)
    sr5=lst_rating.count(5)

    s1=(sr1/lt)*100
    s2=(sr2/lt)*100
    s3=(sr3/lt)*100
    s4=(sr4/lt)*100
    s5=(sr5/lt)*100




    context={'head1':head1,'head2':head2,'j1':j1,'emplo1':emplo1,'jo':jo,'lt':lt,'s1':s1,'s2':s2,'s3':s3,'s4':s4,'s5':s5,'sr1':sr1,'sr2':sr2,'sr3':sr3,'sr4':sr4,'sr5':sr5,}

    return render(request,'emp/main_index.html',context)







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


def GeneratePdf(request):
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




# ----------------------just a basic attempt o(n^2) algo for recommending

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

# main page job gallery

def job_gallery():
    name =jobs.objects.all()

    lst = []
    rec_lst = []
    sk = []
    for jb in name:
        p = jb.appliedjobs_set.all()
        for j in p:
            stud = j.student.all()
            st_skill = stud[0].skills.split(',')
            job_skills = jb.jobskills.split(',')
            for j in st_skill:
                j = j.lower()
                sk.append(j)
            st_skill = sk
            st_skill = set(st_skill)
            job_skills = set(job_skills)
            val1 = job_skills.intersection(st_skill)
            val2 = job_skills.union(st_skill)
            sim = len(val1) / len(val2)
            print(sim)
            if sim > 0.0:
                lst.append(stud[0])

        rec_lst.append(lst)
        lst = []


    return rec_lst

@login_required(login_url='login')
@employers_only
@allowed_users(allowed_roles=['students'])

# only for students.....-----------------------Student main dashboard


def studentpg(request):
    jb = jobs.objects.all()

    jo = len(jb)

    head1 = jb[(jo - 5):]

    emplo = employer.objects.all()
    emplo1 = len(emplo)
    uname=request.user.student.name

    s=[]
    context = {'head1': head1,'s':s}
    if request.user.student.name==" ":
        #job=jobs.objects.all()
        #print(s)

        return render(request, 'emp/student_section.html',context)
    else:
        ustatus=1
        a1 = appliedjobs.objects.filter(student__name__startswith=request.user.student)
        if len(a1)==1:

            date = a1[0].date_created
        # print(a1.student.all())

            data = a1[0].jobs.all()

            s.append(request.user.student.mail)
            k=len(data)
            print(s)
            data=data[0:10]
            context = {'data': data, 'date': date,'head1':head1,'s':s}
            return render(request,'emp/student_section.html',context)



    return render(request, 'emp/student_section.html',context)


def more_jobs(request):
    a1 = appliedjobs.objects.filter(student__name__startswith=request.user.student)
    if len(a1) == 1:
        date = a1[0].date_created
    # print(a1.student.all())

    data = a1[0].jobs.all()
    k = len(data)

    context = {'data': data, 'date': date}
    return render(request, 'emp/jobs_more.html', context)


# only students
#----------------------------------------------for student profile settings


@allowed_users(allowed_roles=['students'])
def student_profile(request):
    student=request.user.student
    form=studentform(instance=student)

    if request.method =='POST':
        form=studentform(request.POST, request.FILES,instance=student)
        if form.is_valid():
            fname=form.cleaned_data.get(' upload_your_work')

            form.save()
            messages.success(request, "your profile has been created! Now you can apply for jobs")

    name=student.name
    print(len(name))
    k=len(name)
    k=k-1
    s=k
    context={'form':form,'k':k,'s':s}
    #messages.success(request,"profile updated")
    return render(request,'emp/student_profile.html',context)

#-----------------------------------------------student profile card (CV)


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
    users = User.objects.all()
    ls=[]
    for i in users:
        ls.append(i)
    print(users)
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


#!-------------------------------------------------update job details
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

# students apply to company's Job (jacard sim for job display in students sections)

def apply_to_particular(request,pk):
    jb=jobs.objects.get(id=pk)
    cp=request.user.employer
    name=request.user.employer.jobs_set.all()
    lst=[]
    if jb in name:
        p=jb.appliedjobs_set.all()
        k=len(p)
        for j in p:

            stud = j.student.all()
            lst.append(stud[0])
        print(lst)

    company_name=jb.employer.company_name
    lst = []
    selected = []
    sk = []
    lst_recom = []
    if jb in name:
        p = jb.appliedjobs_set.all()
        k = len(p)
        for j in p:
            stud = j.student.all()
            print(stud)
            st_skill = stud[0].skills.split(',')
            print(st_skill)
            job_skills = jb.jobskills.split(',')
            for j in st_skill:
                j = j.lower()
                sk.append(j)
            st_skill = sk
            sk=[]
            st_skill = set(st_skill)
            job_skills = set(job_skills)
            val1 = job_skills.intersection(st_skill)
            val2 = job_skills.union(st_skill)
            sim = len(val1) / len(val2)
            #print(sim)
            if sim >= 0.3:
                lst_recom.append(stud[0])
                print(sim)
                print(lst_recom)

            # s = student_status.objects.filter(name=stud[0].name)

            lst.append(stud[0])

    jt = student_status.objects.filter(jobs_id=jb)
    for i in jt:
        if i.student.name not in selected:
            selected.append(i.student.name)

    #print(company_name)
    context={'item':jb,'appli':k,'stu':lst,'lst': lst,'jb':jb,'lst_recom':lst_recom,'selected':selected}
    return render(request,'emp/company_card.html',context)

# list of students applied in job to company and recommend students to company

def student_list(request,pk,pk1):
    jb=jobs.objects.get(id=pk)
    name = request.user.employer.jobs_set.all()
    lst = []
    selected=[]
    sk=[]
    lst_recom=[]
    if jb in name:
        p = jb.appliedjobs_set.all()
        k = len(p)
        for j in p:
            stud = j.student.all()
            st_skill = stud[0].skills.split(',')
            print(st_skill)
            job_skills = jb.jobskills.split(',')
            for j in st_skill:
                j = j.lower()
                sk.append(j)
            st_skill=sk
            st_skill = set(st_skill)
            job_skills = set(job_skills)
            val1 = job_skills.intersection(st_skill)
            val2 = job_skills.union(st_skill)
            sim = len(val1) / len(val2)
            print(1)
            if sim>=0.4:
                print(sim)
                lst_recom.append(stud[0])
            print(lst_recom)






            lst.append(stud[0])

    jt = student_status.objects.filter(jobs_id=jb)
    for i in jt:
        if i.student.name not in selected:
            selected.append(i.student.name)





    context = {'lst': lst,'jb':jb,'lst_recom':lst_recom,'selected':selected}






    return render(request,'emp/student_lists.html',context)



def recommended_jobs(request):

    rec_lst=job_gallery()
    context={'rec_lst':rec_lst}
    return  render(request,'emp/students_recomm.html',context)

    return HttpResponse("404")

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
    if request.user.student.name == " ":
        messages.success(request, 'Create your profile before applying for jobs')
        return redirect('/')
    else:
        query=request.GET.get('search')
        head=[]
        query=str(query)

        titlejobs=jobs.objects.values('jobtitle','id')      #list of dict

        title={item['jobtitle'] for item in titlejobs}
        lst=list(title) # set of job titles
        print(lst)

        titletemp=jobs.objects.filter(jobskills__icontains=query)

        head=titletemp
        if len(head)==0:
            return render(request, 'emp/not_found.html')

        context={'head':head}

        return render(request,'emp/searchjob.html',context)

        return HttpResponse("no item found.Search for job title like Django developer , Java developer")


#!------------------------------showcasing all jobs to students posted by companies no filtering initially.will apply later
# for students

@allowed_users(allowed_roles=['students'])
def apply_jobs(request):
    if request.user.student.name==" ":
        messages.success(request, 'Create your profile before applying for jobs')
        return render(request,'emp/student_section.html')
    else:
        job=[]
        a1 = appliedjobs.objects.filter(student__name__startswith=request.user.student)
        #applied=a1.jobs.all()
        #print(applied)
        alljobs = jobs.objects.all()
        stud = request.user.student
        ds=stud.skills.split(',')
        for jobb in alljobs:
            dj = jobb.jobskills.split(',')
            for d in ds:

                if d in dj:
                    job.append(jobb)
                    break
        #job=jobs.objects.all()
        s1=request.user.student


        total=len(job)
        print(job)
        #job=list(set(job)-set(applied))
        context={'job':job}



        return render(request,'emp/apply.html',context)
    return HttpResponse("404 NOT FOUND")

# for students
#  student will apply for jobs
# used appliedjobs models to access (many to many field)
@allowed_users(allowed_roles=['students'])

def company_info(request,pk):
    jb=jobs.objects.get(id=pk)
    p=jb.appliedjobs_set.all()
    k=len(p)
    print(jb.employer.company_name)
    context={'item':jb,'appli':k}
    return render(request,'emp/info_company.html',context)

def latest_update():
    jb = jobs.objects.all()

    jo = len(jb)

    head1 = jb[(jo - 3):]

    emplo = employer.objects.all()
    emplo1 = len(emplo)
    context={'head1':head1}
    return context

#job applied by students
def jobs_applied(request,pk):
    application=appliedjobs.objects.all()
    st=request.user.student                          #student object
    jb = jobs.objects.get(id=pk)                     # job object
    #print(jb.jobskills)
    context1=latest_update()
    a1=appliedjobs.objects.filter(student__name__startswith=request.user.student)                                #applied objects
    if len(a1)==1:
        a1[0].jobs.add(jb)
        print(a1)
        a1[0].save()
        date=a1[0].date_created
    #print(a1.student.all())

        data=a1[0].jobs.all()
        context={'data':data,'date':date}
        return redirect('/')
    else:
        a1=appliedjobs()
        a1.save()
        a1.jobs.add(jb)
        a1.student.add(st)

        data = a1.jobs.all()
        date = a1.date_created
        context = {'data': data, 'date': date}
        messages.success(request, "Your application has been sent successfully for")
        return redirect('/')


    p=application[1].jobs.all()

    return HttpResponse("404 not found")

@allowed_users(allowed_roles=['employer'])
def students_to_employer(request):

    name = request.user.employer.jobs_set.all()    # query set of posted jobs
    student_list=[]
    lst=[]


    for i in name:
        lst.append(i)
        p=i.appliedjobs_set.all()
        for j in p:

            job_applied=i
            stud=j.student.all()
           # print(stud[0].skills)
            sk=[]
            student_skill=stud[0].skills.split(',')
            for j in student_skill:
                j=j.lower()
                sk.append(j)

            job_skills=i.jobskills.split(',')


            lst.append(stud[0])


        k = len(lst) - 1
        lst.insert(0,k)
        student_list.append(lst)





    context={'student_list':student_list}
    return render(request,'emp/students_to_employer.html',context)
    return HttpResponse("404 not found")


@allowed_users(allowed_roles=['employer'])
def student_reoprt(request):
    name = request.user.employer.jobs_set.all()
    student_list=[]
    datas=[]

    for i in name:

        p=i.appliedjobs_set.all()
        for j in p:

            stud=j.student.all()
            if stud[0] not in datas:
                datas.append(stud[0])

    #print(datas)
    context={'datas':datas}
    return render(request,'emp/student_report.html',context)
    return HttpResponse("404 not found")

def my_report(request,pk2,pk):
    su=student.objects.get(id=pk)
    print(su)
    context={'data':su}
    return render(request, 'emp/student_report.html', context)

def st_report(request,pk):
    su=student.objects.get(id=pk)
    print(su)
    context={'data':su}
    return render(request, 'emp/student_report.html', context)


#---------------------------------------------------------MAIN  PAGE SEARCH FUNCTIONS-----------------------------------


def search_job_skills(request):

        query = request.GET.get('search1')
        head = []
        query = str(query)

        titletemp = jobs.objects.filter(jobskills__icontains=query)


        head = titletemp
        if len(head)>=1:

            context = {'head': head}

            return render(request, 'emp/search_job_skills.html', context)
        else:
           return render(request,'emp/not_found.html')


def search_job_title(request):
    query = request.GET.get('search2')
    head = []
    query = str(query)

    titletemp = jobs.objects.filter(jobtitle__icontains=query)

    head = titletemp
    if len(head) >= 1:

        context = {'head': head}

        return render(request, 'emp/search_job_title.html', context)
    else:
        return render(request, 'emp/not_found.html')


def search_student(request):
    query = request.GET.get('search4')
    head = []
    query = str(query)

    titletemp = student.objects.filter(skills__icontains=query)

    head = titletemp
    if len(head) >= 1:

        context = {'head': head}
        print(context)
        return render(request, 'emp/search_student.html',context)
    else:
        return render(request, 'emp/not_found.html')


def recruiters(request):
    query = request.GET.get('search3')
    title=employer.objects.filter(company_name__icontains=query)
    print(title)
    head=[]
    head=title
    if len(head)>=1:
        context = {'head': head}

        return render(request, 'emp/recruiters.html', context)
    else:
        return render(request, 'emp/not_found.html')






def contact_student(request):
    if request.method=='POST':
        name=request.user
        email=request.user.email
        message=request.POST['message']
        ask=contact_stu(name=name,email=email,message=message)
        ask.save()
        send_mail('Spoken Recommendation', 'Thank You for contacting us! we will reach to you soon'
                  , settings.EMAIL_HOST_USER,
                  [email], fail_silently=False
                  )
        return redirect('student')


# Main page
def feedback(request):
    if request.method=='POST':
        name=request.POST['name1']
        email1=request.POST['email1']
        rating=request.POST['ur']

        suggestion=request.POST['message']

        user_rate=rate(name=name,email=email1,rating=rating,suggestion=suggestion)
        user_rate.save()


        return redirect('/')



    return render(request,'emp/rate.html')

#company section to accept students

def accept(request,pk,pk1,pk3):

    st=student.objects.get(id=pk)
    jb=jobs.objects.get(id=pk3)

    comp=jb.employer.company_name
    ename=jb.employer.emp_name
    jtitle=jb.jobtitle

    statu=1

    db=student_status(student=st,jobs=jb,comp=comp,ename=ename,jtitle=jtitle,statu=statu)
    db.save()



    p = st.appliedjobs_set.all()
    print(jb)
    return redirect("/")


# blog spoken

def blogHome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,'emp/blogHome.html',context)

def blogPost(request, slug):
    article=Post.objects.filter(slug=slug).first()
    comments=blogcomment.objects.filter(post=article,parent=None)
    replies = blogcomment.objects.filter(post=article).exclude(parent=None)
    repdict={}
    for reply in replies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno]=[reply]
        else:
            repdict[reply.parent.sno].append(reply)
    context={'article':article,'comments':comments,'user':request.user,'repdict':repdict}
    return render(request,'emp/blogPost.html',context)


def postcomment(request):
    if request.method=="POST":
        comment=request.POST.get("comment")
        user=request.user
        postsno=request.POST.get("postsno")
        post=Post.objects.get(sno=postsno)
        parentsno=request.POST.get('parentsno')
        if parentsno=="":
            comm = blogcomment(comment=comment, user=user, post=post)
            comm.save()
            messages.success(request, "comment posted")
        else:
            parent=blogcomment.objects.get(sno=parentsno)
            comm = blogcomment(comment=comment, user=user, post=post,parent=parent)





            comm.save()
            messages.success(request,"reply posted")
    return redirect(f"/blog/{post.slug}")


def blogStudenthome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'emp/blogStudent_home.html', context)

def studentblogPost(request,slug):
    article = Post.objects.filter(slug=slug).first()
    comments = blogcomment.objects.filter(post=article, parent=None)
    replies = blogcomment.objects.filter(post=article).exclude(parent=None)
    repdict = {}
    for reply in replies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno] = [reply]
        else:
            repdict[reply.parent.sno].append(reply)
    context = {'article': article, 'comments': comments, 'user': request.user, 'repdict': repdict}
    return render(request, 'emp/blogStudent_post.html', context)


def studentpostcomment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postsno = request.POST.get("postsno")
        post = Post.objects.get(sno=postsno)
        parentsno = request.POST.get('parentsno')
        if parentsno == "":
            comm = blogcomment(comment=comment, user=user, post=post)
            comm.save()
            messages.success(request, "comment posted")
        else:
            parent = blogcomment.objects.get(sno=parentsno)
            comm = blogcomment(comment=comment, user=user, post=post, parent=parent)

            comm.save()
            messages.success(request, "reply posted")
    return redirect(f"/blogstudent/{post.slug}")

# payment paytm/cards
def checkout(request):
    if request.method=="POST":


        amount =1000
        cmp=request.user.employer
        email = request.user.email
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')

        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order =pay(address=address,zip_code=zip_code, phone=phone, amount=amount,employer=cmp)
        order.save()
        update =payUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #return render(request, 'home/payment.html', {'thank':thank, 'id': id})
        # Request payTm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'xNKSRQ79886016844144',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'emp/paytm.html', {'param_dict': param_dict})

    return render(request, 'emp/payment.html')
MERCHANT_KEY='XXXXXXXX'
@csrf_exempt
def handlerequest(request):
    form=request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'home/paymentstatus.html', {'response': response_dict})




