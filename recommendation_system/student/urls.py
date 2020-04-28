from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="studenthome"),
    path("apply/", views.apply, name="apply"),
]