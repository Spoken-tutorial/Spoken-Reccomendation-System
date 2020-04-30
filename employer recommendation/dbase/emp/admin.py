from django.contrib import admin

# Register your models here.
from .models import employer,jobs,student,appliedjobs

admin.site.register(employer)
admin.site.register(jobs)
admin.site.register(student)
admin.site.register(appliedjobs)
