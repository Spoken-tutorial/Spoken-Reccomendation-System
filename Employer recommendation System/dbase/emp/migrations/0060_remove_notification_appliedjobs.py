# Generated by Django 3.0.5 on 2020-05-09 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0059_notification_appliedjobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='appliedjobs',
        ),
    ]
