from django import template
from main import models
from django.contrib.auth.models import User
from datetime import datetime
# استيراد وحدة timezone
from django.utils import timezone


register = template.Library()

@register.simple_tag
def check_user_package(user_id,plan_id):
  user=User.objects.get(id=user_id)
  plan = models.SubPlan.objects.get(id=plan_id)
  check_package = models.Subscription.objects.filter(user=user,plan=plan).count()

  if check_package > 0:
    return True
  else:
    return False
  


  
@register.simple_tag
def check_package_validity(user_id,plan_id):
  expired=False
  user=User.objects.get(id=user_id)
  plan = models.SubPlan.objects.get(id=plan_id)
  check_package = models.Subscription.objects.filter(user=user,plan=plan).count()

  if check_package > 0:
    pdata = models.Subscription.objects.filter(user=user,plan=plan).order_by('-id').first()
    today = timezone.now()  # تاريخ اليوم بتوقيت الموقع
    pdate = pdata.reg_date
    # 17 - 19
    pdays=(today - pdate).days
    pvalidity=pdata.plan.validity_days
    if pdays > pvalidity:
      expired=True
  else:
    expired=False


