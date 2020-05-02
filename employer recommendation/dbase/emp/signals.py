from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User, Group
from .models import student,employer


@receiver(post_save, sender=User)
def student_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='students')
        instance.groups.add(group)

        student.objects.create(user=instance,name=instance.username)

post_save.connect(student_profile,sender=User)


#def employer_profile(sender,instance,created,**kwargs):
 #   if created:
  #      group=Group.objects.get(name='employer')
   #     instance.groups.add(group)
    #    employer.objects.create(user=instance,name=instance.username)
#post_save.connect(employer_profile,sender=User)


# post_save.connect(create_profile, sender=User)

#@receiver(post_save, sender=User)
#def update_profile(sender, instance, created, **kwargs):
 #   if created == False:
  #      instance.student.save()
   #     print('Profile updated!')

# post_save.connect(update_profile, sender=User)