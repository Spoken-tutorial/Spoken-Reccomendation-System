# Generated by Django 3.0.5 on 2020-05-05 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0041_auto_20200505_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='github',
            field=models.URLField(blank=True, default=' ', max_length=300, null=True),
        ),
    ]
