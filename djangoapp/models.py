from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    followers = models.IntegerField(null=True)
    timeupdated = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        db_table = "profile"
        managed = False
    @receiver(post_save,sender=User)
    def update_profile_signal(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()
class Repositories(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='repos',null=True)
    repo = models.CharField(max_length=128,null=True)
    stars= models.IntegerField(null=True)
    class Meta:
        ordering=['-stars']