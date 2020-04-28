from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="emphome"),
    path("postjob/",views.postjob,name="postjob"),

]