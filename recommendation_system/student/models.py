from django.db import models

# Create your models here.
class student(models.Model):

    name=models.CharField(max_length=50,default=" ")
    skills=models.CharField(default="",max_length=200)
    experience=models.CharField(default="",max_length=300)


    def __str__(self):
        return self.name
