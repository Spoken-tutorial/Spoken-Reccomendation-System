from django.db import models

# Create your models here.



class employer(models.Model):

    company_name=models.CharField(max_length=50)


    def __str__(self):
        return self.company_name

class jobs(models.Model):

    job_title=models.CharField(max_length=20,default=" ")
    joblocation=models.CharField(max_length=20)
    jobskills=models.CharField(max_length=50)
    jobdescription=models.CharField(max_length=200)

    def __str__(self):
        return self.jobtitle



