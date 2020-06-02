import django_filters
from .models import *

class jobfilter(django_filters.filterset):
    class Meta:
        model=jobs
        fields='_all_'