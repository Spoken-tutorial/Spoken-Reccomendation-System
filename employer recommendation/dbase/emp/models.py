from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime


# employer profile
class employer(models.Model):
    user=models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    emp_name=models.CharField(default=" ",max_length=50)
    company_name=models.CharField(max_length=50)
    logo=models.ImageField(default='pro1.png',null=True, blank=True)
    company_description = models.TextField(max_length=200,default=" ")
    emp_field=models.CharField(default=" ",max_length=50)
    date_created = models.DateField(auto_now_add=True, null=True)
    e_pic=models.ImageField(default='pro1.png',null=True, blank=True)


    def __str__(self):
        return self.company_name

# jobs he want to post
class jobs(models.Model):

    jobtitle=models.CharField(max_length=20,default=" ")
    joblocation=models.CharField(max_length=20)
    jobskills=models.TextField(max_length=50)
    jobdescription=models.TextField(max_length=200)
    jobcategory=models.CharField(max_length=100,default=" ")
    criteria= models.CharField(max_length=100,default=" ")
    employer=models.ForeignKey(employer,null=True,on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(default="On Review", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.jobtitle

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))
# students profile
class student(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,default=" ")
    mail=models.CharField(max_length=100,default=" ",blank=True,null=True)
    phno=models.CharField(max_length=10,default=0,blank=True,null=True)
    address=models.CharField(max_length=400,default=" ",blank=True)

    education = models.CharField(max_length=30,default=" ")
    degree=models.CharField(max_length=100,default=" ",null=True,blank=True)
    startyear=models.IntegerField(('startyear'), choices=YEAR_CHOICES, default=datetime.datetime.now().year,blank=True)
    endyear = models.IntegerField(('endyear'),choices=YEAR_CHOICES,default=datetime.datetime.now().year, blank=True)
    gpa=models.CharField(max_length=1,default=0,blank=True,null=True)
    skills=models.CharField(default="",max_length=200)
    experience=models.TextField(default=" ",max_length=1000)


    Spokentest_score = models.FloatField(default=0.0)
    about=models.TextField(max_length=2000, default=" ", blank=True, null=True)
    pic = models.ImageField(default='pro1.png',null=True, blank=True)
    github = models.URLField(default=" ", max_length=300, blank=True, null=True)
    Linkedin=models.URLField(default=" ", max_length=300, blank=True, null=True)
    upload_your_work=models.FileField(upload_to='documents/',null=True,blank=True)
    date_created=models.DateField(auto_now_add=True,null=True)




    def __str__(self):
        return self.name
class appliedjobs(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True,blank=True)
    jobs = models.ManyToManyField(jobs,blank=True)
    student=models.ManyToManyField(student,blank=True)





