from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# employer profile
class employer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    emp_name=models.CharField(default=" ",max_length=50)
    company_name=models.CharField(max_length=50)
    company_description = models.CharField(max_length=200,default=" ")
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


    def __str__(self):
        return self.jobtitle


# students profile
class student(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,default=" ")
    education = models.CharField(max_length=30,default=" ")
    skills=models.CharField(default="",max_length=200)
    experience=models.CharField(default="",max_length=300)
    performance_score = models.FloatField(default=0.0)
    pic = models.ImageField(default='pro1.png',null=True, blank=True)
    date_created=models.DateField(auto_now_add=True,null=True)



    def __str__(self):
        return self.name
class appliedjobs(models.Model):

    jobs = models.ManyToManyField(jobs,null=True)
    student=models.ManyToManyField(student,null=True)





