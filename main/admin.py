from django.contrib import admin
from . import models
# Register your models here.

class BannerAdmin(admin.ModelAdmin):
  list_display = ('alt_text','image_tag')

admin.site.register(models.Banners,BannerAdmin)

class ServiceAdmin(admin.ModelAdmin):
  list_display = ('title','image_tag')

admin.site.register(models.Service,ServiceAdmin)


class PageAdmin(admin.ModelAdmin):
  list_display = ('title',)

admin.site.register(models.Page,PageAdmin)


class FAQAdmin(admin.ModelAdmin):
  list_display = ('quest',)

admin.site.register(models.FAQ,FAQAdmin)



class EnquiryAdmin(admin.ModelAdmin):
  list_display = ('full_name','email', 'detail','create_at')

admin.site.register(models.Enquiry,EnquiryAdmin)



class GalleryAdmin(admin.ModelAdmin):
  list_display = ('title','image_tag')

admin.site.register(models.Gallery,GalleryAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
  list_display = ('alt_text','image_tag')

admin.site.register(models.GalleryImage,GalleryImageAdmin)



class SubPlanAdmin(admin.ModelAdmin):
  list_editable = ['price','max_members']
  list_display = ('title','max_members','validity_days','price')

admin.site.register(models.SubPlan,SubPlanAdmin)


class SubPlanFeatureAdmin(admin.ModelAdmin):
  list_display = ('title','subplans')
  # اسم الليست هوا اللذي مرر فوق 
  # | وهنا يقوم بعرض الخطط وبينهم هذا 
  def subplans(self,obj):
    return " | ".join([sub.title for sub in obj.subplan.all()])

admin.site.register(models.SubPlanFeature,SubPlanFeatureAdmin)



class TotalDiscountAdmin(admin.ModelAdmin):
  list_display = ('total_months','total_discount')

admin.site.register(models.TotalDiscount,TotalDiscountAdmin)



class SubscriberAdmin(admin.ModelAdmin):
  list_display = ('subs','mobile','image_tag')

admin.site.register(models.Subscriber,SubscriberAdmin)




class SubscriptionAdmin(admin.ModelAdmin):
  list_display = ('user','plan','reg_date','price')

admin.site.register(models.Subscription,SubscriptionAdmin)





class TrainerAdmin(admin.ModelAdmin):
  list_editable = ['is_active']
  list_display = ('full_name','mobile','salary','is_active','image_tag')

admin.site.register(models.Trainer,TrainerAdmin)




class NotifyAdmin(admin.ModelAdmin):
  
  list_display = ('not_detail', 'read_by_user', 'read_by_trainer',)

admin.site.register(models.Notify,NotifyAdmin)


class NotifUserStatusAdmin(admin.ModelAdmin):
  
  list_display = ('notif', 'user', 'status',)

admin.site.register(models.NotifUserStatus,NotifUserStatusAdmin)


class AssignSubscriberAdmin(admin.ModelAdmin):
  
  list_display = ('trainer','user')

admin.site.register(models.AssignSubscriber,AssignSubscriberAdmin)



class TrainerAchivementAdmin(admin.ModelAdmin):
  
  list_display = ('title','image_tag')

admin.site.register(models.TrainerAchivement,TrainerAchivementAdmin)



class TrainerSalaryAdmin(admin.ModelAdmin):
  
  list_display = ('trainer','amt','amt_date')

admin.site.register(models.TrainerSalary,TrainerSalaryAdmin)




class TrainerNotificationAdmin(admin.ModelAdmin):
  
  list_display = ('notif_msg',)

admin.site.register(models.TrainerNotification,TrainerNotificationAdmin)






class NotifTrainerStatusAdmin(admin.ModelAdmin):
  
  list_display = ('notif',)

admin.site.register(models.NotifTrainerStatus,NotifTrainerStatusAdmin)





class TrainerMsg(admin.ModelAdmin):
  
  list_display = ('user','trainer','message')

admin.site.register(models.TrainerMsg,TrainerMsg)




class TrainerSubscriberReport(admin.ModelAdmin):
  
  list_display = ('report_for_trainer', 'report_for_user', 'report_from_trainer', 'report_from_user', 'report_msg', )

admin.site.register(models.TrainerSubscriberReport,TrainerSubscriberReport)







