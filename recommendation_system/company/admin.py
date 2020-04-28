from django.contrib import admin

# Register your models here.
from .models import employer,jobs
admin.site.register(employer)
admin.site.register(jobs)
