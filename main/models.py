from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
# from django.utils.safestring import mark_safe
# Create your models here.


class Banners(models.Model):
  img = models.ImageField(upload_to='banners/')
  alt_text = models.CharField(max_length=150)

  class Meta:
     verbose_name_plural = "Banners"

  def __str__(self):
      return self.alt_text
  
  def image_tag(self):
     return mark_safe('<img src="%s" width="80" height="30" />' % (self.img.url))
  

class Service(models.Model):
   title = models.CharField(max_length=150)
   detail = models.TextField()
   img = models.ImageField(upload_to='service/',null=True)


   def __str__(self):
      return self.title
  
   def image_tag(self):
     return mark_safe('<img src="%s" width="80" height="30" />' % (self.img.url))
   


class Page(models.Model):
   title = models.CharField(max_length=200)
   detail = models.TextField()

   def __str__(self):
       return self.title
   



class FAQ(models.Model):
   quest = models.TextField()
   ans = models.TextField()

   def __str__(self):
       return self.quest
   


class Enquiry(models.Model):
   full_name= models.CharField(max_length=100)
   email = models.CharField(max_length=100)
   detail = models.TextField()
   create_at = models.DateTimeField(auto_now_add=True)

   
   class Meta:
     verbose_name_plural = "Enquiries"

   def __str__(self):
       return self.full_name
   


class Gallery(models.Model):
   title = models.CharField(max_length=150)
   detail = models.TextField()
   img = models.ImageField(upload_to='gallery/')

   class Meta:
     verbose_name_plural = "Galleries"

   def __str__(self):
      return self.title
  
   def image_tag(self):
     return mark_safe('<img src="%s" width="80" height="30" />' % (self.img.url))
   


class GalleryImage(models.Model):
   gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE,null=True)
   alt_text = models.CharField(max_length=150)
   img = models.ImageField(upload_to='galleryImgs/')


   def __str__(self):
      return self.alt_text
  
   def image_tag(self):
     return mark_safe('<img src="%s" width="80" height="30" />' % (self.img.url))
   



class SubPlan(models.Model):
   title = models.CharField(max_length=150)
   max_members = models.IntegerField(default=0)
   price = models.IntegerField()
   validity_days = models.IntegerField(null=True)

   def __str__(self):
       return self.title
   

class SubPlanFeature(models.Model):
   subplan = models.ManyToManyField(SubPlan)
   title = models.CharField(max_length=150)

   def __str__(self):
       return self.title
   


class TotalDiscount(models.Model):
   subplan = models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
   total_months = models.IntegerField()
   total_discount = models.IntegerField()

   def __str__(self):
       return str(self.total_months)
   


class Subscriber(models.Model):
   subs = models.ForeignKey(User, on_delete=models.CASCADE)
   mobile = models.CharField(max_length=20)
   address = models.TextField()
   img = models.ImageField(upload_to='subscriber/')
   
   def __str__(self):
      return str(self.subs)
  
   def image_tag(self):
     if self.img:
      return mark_safe('<img src="%s" width="80" height="30" />' % (self.img.url))
     else:
        return 'No Image!'
   

@receiver(post_save,sender=User)
def create_subscriber(sender,instance,created,**kwargs):
   if created:
      Subscriber.objects.create(subs=instance)

class Subscription(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   plan = models.ForeignKey(SubPlan, on_delete=models.CASCADE)
   price = models.CharField(max_length=50)
   reg_date = models.DateTimeField(auto_now_add=True,null=True)


class Trainer(models.Model):
   full_name = models.CharField(max_length=50)
   username = models.CharField(max_length=100,null=True)
   pwd = models.CharField(max_length=100,null=True)
   mobile = models.CharField(max_length=50)
   address = models.TextField()
   is_active = models.BooleanField(default=False)
   detail = models.TextField()
   img = models.ImageField(upload_to='trainers/')
   salary = models.IntegerField(default=0)

   facebook = models.CharField(max_length=100,null=True)
   twiter = models.CharField(max_length=100,null=True)
   youtube = models.CharField(max_length=100,null=True)
   pinterst = models.CharField(max_length=100,null=True)
  
   def image_tag(self):
     if self.img:
      return mark_safe('<img src="%s" width="80" height="70" />' % (self.img.url))
     else:
        return 'No Image!'

   def __str__(self):
       return self.full_name
   



class Notify(models.Model):
   not_detail = models.TextField()
   read_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
   read_by_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True,blank=True)
   
   class Meta:
     verbose_name_plural = "Notifies"

   def __str__(self):
       return self.not_detail
   


class NotifUserStatus(models.Model):
   notif=models.ForeignKey(Notify,on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   status = models.BooleanField(default=False)




class AssignSubscriber(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
   trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
   

   def __str__(self):
       return str(self.user)
   


class TrainerAchivement(models.Model):
   trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
   title = models.CharField(max_length=50)
   detail = models.TextField()
   img = models.ImageField(upload_to='trainers-achivement/')

   def __str__(self):
       return str(self.trainer)
   
   def image_tag(self):
     if self.img:
      return mark_safe('<img src="%s" width="80" height="70" />' % (self.img.url))
     else:
        return 'No Image!'
     


class TrainerSalary(models.Model):
   trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
   amt = models.IntegerField()
   amt_date = models.DateField()
   remarks = models.TextField(blank=True)


   def __str__(self):
       return (self.trainer.full_name)
   



class TrainerNotification(models.Model):
   notif_msg = models.TextField()

   def __str__(self):
       return self.notif_msg
   
   def save(self,*args, **kwargs):
      super(TrainerNotification,self).save(*args, **kwargs)
      channel_layer = get_channel_layer()
      notif=self.notif_msg
      total = TrainerNotification.objects.all().count()
      async_to_sync(channel_layer.group_send)(
         'noti_group_name',{
          'type': "send_notification",
          'value':json.dumps({'notif':notif,'total':total})
         }
      )
      

class NotifTrainerStatus(models.Model):
   notif=models.ForeignKey(TrainerNotification,on_delete=models.CASCADE)
   trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
   status = models.BooleanField(default=False)



class TrainerMsg(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
   message = models.TextField()
   


class TrainerSubscriberReport(models.Model):
    report_for_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True,related_name='report_for_trainer')
    report_for_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='report_for_user')
    report_from_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True,related_name='report_from_trainer')
    report_from_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='report_from_user')
    report_msg = models.TextField()

