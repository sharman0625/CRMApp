from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import Customer, User


@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:       
        group = Group.objects.get(name='Customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance,name=instance.username)   # Here : instance = user
        print('Profile created')
        
# post_save.connect(customer_profile, sender=User)