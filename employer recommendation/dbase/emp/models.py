from django.db import models

# Create your models here.



class employer(models.Model):

    company_name=models.CharField(max_length=50)
    company_description = models.CharField(max_length=200,default=" ")



    def __str__(self):
        return self.company_name

class jobs(models.Model):

    jobtitle=models.CharField(max_length=20,default=" ")
    joblocation=models.CharField(max_length=20)
    jobskills=models.CharField(max_length=50)
    jobdescription=models.CharField(max_length=200)
    test_score = models.FloatField(default=0.0)
    employer=models.ForeignKey(employer,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.jobtitle


# Create your models here.
class student(models.Model):

    name=models.CharField(max_length=50,default=" ")
    education = models.CharField(max_length=30,default=" ")
    skills=models.CharField(default="",max_length=200)
    experience=models.CharField(default="",max_length=300)
    performance_score = models.FloatField(default=0.0)
    #jobs=models.ForeignKey(jobs,null=True,on_delete=models.CASCADE)
    #jobs=models.ManyToManyField(jobs)

    def __str__(self):
        return self.name
class appliedjobs(models.Model):
    jobs = models.ManyToManyField(jobs)
    student=models.ManyToManyField(student)



from django.db import models

# Create your models here.
