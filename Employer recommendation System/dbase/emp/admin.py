from django.contrib import admin

# Register your models here.
from .models import employer,jobs,student,appliedjobs,Notification,Contact,contact_stu,rate,student_status,Post,blogcomment,pay,payUpdate

admin.site.register(employer)
admin.site.register(jobs)
admin.site.register(student)
admin.site.register(appliedjobs)
admin.site.register(Notification)
admin.site.register(Contact)
admin.site.register(contact_stu)
admin.site.register(rate)
admin.site.register(student_status)
admin.site.register(Post)
admin.site.register(blogcomment)
admin.site.register(pay)
admin.site.register(payUpdate)


