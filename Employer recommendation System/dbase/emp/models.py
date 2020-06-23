from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save


# employer profile
class employer(models.Model):
    user=models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    emp_name=models.CharField(default=" ",max_length=50)
    company_name=models.CharField(max_length=300)
    logo=models.ImageField(default='pro1.png',null=True, blank=True)
    company_description = models.TextField(max_length=2000,default=" ")
    emp_field=models.CharField(default=" ",max_length=400)
    date_created = models.DateField(auto_now_add=True, null=True)
    e_pic=models.ImageField(default='pro1.png',null=True, blank=True)


    def __str__(self):
        return self.company_name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# jobs he want to post
class jobs(models.Model):

    jobtitle=models.CharField(max_length=200,default=" ")
    joblocation=models.CharField(max_length=200)
    jobskills=models.TextField(max_length=500)
    jobdescription=models.TextField(max_length=2000)
    jobcategory=models.CharField(max_length=100,default=" ")
    criteria= models.CharField(max_length=1000,default=" ")
    employer=models.ForeignKey(employer,null=True,on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=True)

    status = models.CharField(default="On Review", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.jobtitle

YEAR_CHOICES = []
for r in range(2015, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

# students profile
class student(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,default=" ")
    mail=models.EmailField(default=" ",blank=True,null=True)
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

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class spoken(models.Model):
    student=models.ForeignKey(student,null=True,on_delete=models.CASCADE)
    programming_languages=models.CharField(max_length=10,null=True,blank=True)
    score=models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.student.name


class appliedjobs(models.Model):

    date_created = models.DateField(auto_now_add=True, null=True,blank=True)
    jobs = models.ManyToManyField(jobs,blank=True)
    student=models.ManyToManyField(student,blank=True)


NOTIFICATION_TARGET = (
    ('1', 'User'),
    ('2', 'students'),
    ('3', 'employer')
)


class Notification(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='notification',null=True)
    actor = models.CharField(max_length=50)
    verb = models.CharField(max_length=50)
    action = models.CharField(max_length=50, blank=True)
    target = models.CharField(
        max_length=1, default='1', choices=NOTIFICATION_TARGET)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #employer = models.ForeignKey(employer, null=True, on_delete=models.CASCADE)
    #student=models.ForeignKey(student,null=True,on_delete=models.CASCADE)
    #appliedjobs=models.ForeignKey(appliedjobs,null=True,on_delete=models.CASCADE)

def __str__(self):
    return f"{self.actor} {self.verb} {self.action} {self.target} at 			{self.timestamp}"


# main page contact

class Contact(models.Model):

    email=models.CharField(max_length=50,default=" ")
    comment=models.CharField(max_length=200,default=" ")

    def __str__(self):
        return self.email

# student contact

class contact_stu(models.Model):
    name=models.CharField(max_length=100,default='')
    email=models.CharField(max_length=200,default='')
    message=models.TextField(max_length=500,default='')


    def __str__(self):
        return self.name





# rating of website from user

class rate(models.Model):
    name=models.CharField(max_length=100,blank=False)
    email=models.CharField(max_length=100,blank=False)
    rating=models.IntegerField(blank=True)
    suggestion=models.TextField(blank=False,max_length=500)
    reply=models.TextField(blank=True,max_length=1000)

    def __str__(self):
        return self.name

# accept student by company

class student_status(models.Model):
    student=models.ForeignKey(student, null=True, on_delete=models.CASCADE)
    jobs=models.ForeignKey(jobs,null=True,on_delete=models.CASCADE)

    comp=models.CharField(max_length=100,blank=False,default='')
    ename=models.CharField(max_length=100,blank=False,default='')
    jtitle=models.CharField(max_length=200,blank=False,default='')
    statu=models.IntegerField(blank=True)

    def __str__(self):
        return self.jtitle

# blog post models

class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=20)


    content=models.TextField()
    author=models.CharField(max_length=20)
    slug= models.CharField(max_length=130)
    timestamp=models.DateTimeField(blank=True)

    def __str__(self):
        return self.title+ 'by'+self.author
class blogcomment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[0:13]+"..."+'by'+" "+self.user.username



class pay(models.Model):
    order_id = models.AutoField(primary_key=True)
    #items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    #name = models.CharField(max_length=90,default='')
    #email = models.CharField(max_length=111)
    address = models.CharField(max_length=111,default='')
    #city = models.CharField(max_length=111)
    #state = models.CharField(max_length=111)
    employer = models.ForeignKey(employer, null=True, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")

class payUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."