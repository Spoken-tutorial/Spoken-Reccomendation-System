# Generated by Django 3.0.5 on 2020-05-01 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emp', '0019_remove_student_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedjobs',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
