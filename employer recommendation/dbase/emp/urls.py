from django.contrib import admin
from django.urls import path
from  . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('apply/', views.apply, name="apply"),
    path('post_jobs/',views.post,name="post_jobs"),
    path('results/',views.recommend,name="results"),
    path('signup',views.signup,name='signup'),
    path('login',views.signin,name='login'),
    path('logout', views.handlelogout, name='logout'),
    path('students',views.student,name="student"),
    path('employer', views.company, name="employer"),

]
