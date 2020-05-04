from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from  . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('apply/', views.apply, name="apply"),
    path('post_jobs',views.create_job,name="post_jobs"),
    path('results/',views.recommend,name="results"),
    path('profile_page',views.student_page,name='profile_page'),
    path('signup_student/',views.registerpage_student,name='signup1'),
    path('signup_employer/', views.registerpage_employer, name='signup2'),
    path('updatejob/<str:pk>/',views.update_job,name='update_job'),
    path('deletejob/<str:pk>/', views.delete_job, name='update_job'),
    path('login',views.signin,name='login'),
    path('logout', views.handlelogout, name='logout'),
    path('roles',views.roles,name='roles'),
    path('students',views.studentpg,name="student"),
    path('employer', views.company, name="employer"),
    path('student_profile',views.profile,name='profile'),
    path('employer_profile', views.employer_profile, name='emprofile'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="emp/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="emp/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="emp/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="emp/password_reset_done.html"),name="password_reset_complete"),



]
