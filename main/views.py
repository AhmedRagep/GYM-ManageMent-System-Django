from django.shortcuts import redirect, render
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from datetime import timedelta
import stripe
from . import models
from . import forms


# Create your views here.
def home(request):
  banners = models.Banners.objects.all()
  imgs = models.GalleryImage.objects.all().order_by('-id')[:9]
  services = models.Service.objects.all().order_by('-id')[:3]

  return render(request,'home.html',{'banners':banners,'services':services,'imgs':imgs})


def page_detail(request,id):
  page = models.Page.objects.get(id=id)
  return render(request,'page.html',{'page':page})



def faq_list(request):
  faq = models.FAQ.objects.all()
  return render(request,'faq.html',{'faq':faq})



def contact_page(request):
  
  return render(request,'contact.html',{})



def enquiry(request):
  if request.POST:
    form = forms.EnquiryForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Enquiry Successfully ..')
      return redirect('home')
  else:
    form = forms.EnquiryForm()
    return render(request,'enquiry.html',{'form':form})
  


def gallery(request):
  galleries = models.Gallery.objects.all().order_by('-id')
  return render(request,'gallery.html',{'galleries':galleries})



def gallery_detail(request,id):
  gallery = models.Gallery.objects.get(id=id)
  gallery_imgs = models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')

  return render(request,'gallery-detail.html',{'galleries':gallery_imgs,'gallery':gallery})



def pricing(request):
  pricing = models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all()
  # تعمل مع postgesql فقط
  # pfeature = models.SubPlanFeature.objects.distinct('title')
  pfeature = models.SubPlanFeature.objects.order_by('title')

  return render(request,'pricing.html',{'pricing':pricing,'pfeature':pfeature})



def checkout(request,plan_id):
  plan = models.SubPlan.objects.get(id=plan_id)
  return render(request,'checkout.html',{'plan':plan})




def signup(request):
  if request.POST:
    form = forms.Signup(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Created Account Successfully.. Login')
      return redirect('login')
  form = forms.Signup()
  return render(request,'registration/signup.html',{'form':form})


stripe.api_key = 'sk_test_51OYr06J7uelPNR7g8PnOsnjDUEDsna9o9XEpc13cy46orQooiopFh5916JgvD5fTsxAMBtkWR76OAAC3Om9dxQ2t00YRR50igg'

def checkout_session(request,plan_id):
  plan = models.SubPlan.objects.get(pk=plan_id)
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': plan.title,
        },
        'unit_amount': plan.price*100,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='http://127.0.0.1:8000/pay_cancel',
    client_reference_id=plan_id
  )
  return redirect(session.url, code=303)



from django.core.mail import EmailMessage
from django.template.loader import get_template
def pay_success(request):
  session = stripe.checkout.Session.retrieve(request.GET['session_id'])
  plan_id = session.client_reference_id
  plan = models.SubPlan.objects.get(pk=plan_id)
  user=request.user
  models.Subscription.objects.create(
    user=user,
    plan=plan,
    price=plan.price
  )
  subject = 'Order Email'
  html_content = get_template('orderemail.html').render({'title':plan.title})
  from_email = 'codinghustler@gmail.com'
  msg = EmailMessage(subject, html_content, from_email, ['viphaker15@gmail.com'])
  msg.content_subtype = "html"  # Main content is now text/html
  msg.send()
  return render(request,'pay_success.html')


def pay_cancel(request):
  return render(request,'pay_cancel.html')




def dashboard(request):
  current_plan = models.Subscription.objects.get(user=request.user)
  my_trainer = models.AssignSubscriber.objects.get(user=request.user)
  enddate = current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)

    # جلب الرسائل
  data = models.Notify.objects.all().order_by('-id')
  # متغير بغير صحيح
  notifStatus=False
  # قائمه فارغه
  jsonData = []
  # مجموع الاشعارات الغير مقروؤه
  totalUnread=0
  # تكرار علي الاشعارات
  for d in data:
    try:
      # متغير به الرسائل المقروؤه من المستخدم الحالي
      notifStatusData = models.NotifUserStatus.objects.get(user=request.user,
                notif=d)
      # لو فيه رسائل
      if notifStatusData:
          # خلي المتغير بصح
          notifStatus=True
    # لو مفيش رسائل قرئها اليوزر
    except models.NotifUserStatus.DoesNotExist:
      # خلي المتغير بغير صحيح
      notifStatus=False
    # الرسالة مش مقروؤه 
    if not notifStatus:
      # زود واحد علي متغير الرسائل غير المقروؤه
      totalUnread +=1
  return render(request,'user/dashboard.html',
              {'current_plan':current_plan,
              'my_trainer':my_trainer,
              'totalUnread':totalUnread,
              'enddate':enddate})



def update_profile(request):
  if request.POST:
    form = forms.ProfileEdit(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
  form = forms.ProfileEdit(instance=request.user)
  return render(request,'user/update_profile.html',{'form':form})



def trainer_login(request):
  if request.POST:
      username = request.POST['username']
      pwd = request.POST['pwd']
      trainer = models.Trainer.objects.filter(username=username,pwd=pwd).count()
      if trainer > 0:
        trainer = models.Trainer.objects.filter(username=username,pwd=pwd).first()
        request.session['trainerLogin']=True
        request.session['trainerid']=trainer.id
        messages.success(request,'SuccessFully..')
        return redirect('trainer_dashboard')
      else:
        messages.warning(request,'Invalid!!')
        return redirect('trainer_login')
  form = forms.TrainerLogin()
  return render(request,'trainer/trainer-login.html',{'form':form})


def trainer_logout(request):
  del request.session['trainerLogin']
  return redirect('trainer_login')



def trainer_dashboard(request):
  return render(request,'trainer/dashboard.html')
  


def trainer_profile(request):
  t_id = request.session['trainerid']
  trainer = models.Trainer.objects.get(pk=t_id)
  if request.POST:
    form = forms.TrainerProfileForm(request.POST,request.FILES,instance=trainer)
    if form.is_valid():
      form.save()
      messages.success(request,'Updated Successfully..')
      return redirect('trainer_dashboard')
  form = forms.TrainerProfileForm(instance=trainer)
  return render(request,'trainer/update_profile.html',{'form':form})
  




def notifs(request):
  data = models.Notify.objects.all().order_by('-id')
  return render(request,'notifs.html',{'data':data})



def get_notifs(request):
  # جلب الرسائل
  data = models.Notify.objects.all().order_by('-id')
  # متغير بغير صحيح
  notifStatus=False
  # قائمه فارغه
  jsonData = []
  # مجموع الاشعارات الغير مقروؤه
  totalUnread=0
  # تكرار علي الاشعارات
  for d in data:
    try:
      # متغير به الرسائل المقروؤه من المستخدم الحالي
      notifStatusData = models.NotifUserStatus.objects.get(user=request.user,
                notif=d)
      # لو فيه رسائل
      if notifStatusData:
          # خلي المتغير بصح
          notifStatus=True
    # لو مفيش رسائل قرئها اليوزر
    except models.NotifUserStatus.DoesNotExist:
      # خلي المتغير بغير صحيح
      notifStatus=False
    # الرسالة مش مقروؤه 
    if not notifStatus:
      # زود واحد علي متغير الرسائل غير المقروؤه
      totalUnread +=1
    # طيف بيانات الرسالة في القايمه
    jsonData.append({
      'pk':d.id,
      'not_detail':d.not_detail,
      'notifStatus':notifStatus
    })
  # رجع البيانات والرسائل غير المقروؤه
  return JsonResponse({'data':jsonData,'totalUnread':totalUnread})


# لتحويل الرسالة الي مقروؤه عند الضغط عليها
def mark_read_notif(request):
  # متغير تاتي قيمته من اجاكس برقم الرسالة
  notif = request.GET['notif']
  # جلب الرسالة
  notif=models.Notify.objects.get(pk=notif)
  # جلب اليوزر الحالي
  user = request.user
  # انشاء رسالة مقروؤه من اليوزر بمعلوماتها التي حصلنا عليها فوق
  models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
  # ارسال متغير به صحيح بعد ذالك
  return JsonResponse({'bool':True})




def trainer_subscribers(request):
  trainer = models.Trainer.objects.get(pk=request.session['trainerid'])
  trainer_subs = models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
  return render(request,'trainer/trainer_subscribers.html',{'trainer_subs':trainer_subs})



def trainer_payments(request):
  trainer = models.Trainer.objects.get(pk=request.session['trainerid'])
  trainer_pay = models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
  return render(request,'trainer/trainer_payments.html',{'trainer_pay':trainer_pay})


def trainer_changepassword(request):
  if request.POST:
    new_pass = request.POST['new_pass']
    update_pass = models.Trainer.objects.filter(pk=request.session['trainerid']).update(pwd=new_pass)
    if update_pass:
      messages.success(request,"Password Changed Successfully")
      del request.session['trainerLogin']
      return redirect('trainer_login')
    else:
      messages.warning(request,"Error Try Again")
      return redirect('trainer_changepassword')
  form = forms.TrainerChangePassForm
  return render(request,'trainer/trainer_changepassword.html',{'form':form})





def trainer_notifs(request):
  data = models.TrainerNotification.objects.all( ).order_by("-id")
  trainer = models.Trainer.objects.get(id=request.session['trainerid'])
  jsonData=[]
  totalUnread=0
  # تكرار علي الاشعارات
  for d in data:
    try:
      # متغير به الرسائل المقروؤه من المستخدم الحالي
      notifStatusData = models.NotifTrainerStatus.objects.get(trainer=trainer,
                notif=d)
      # لو فيه رسائل
      if notifStatusData:
          # خلي المتغير بصح
          notifStatus=True
    # لو مفيش رسائل قرئها اليوزر
    except models.NotifTrainerStatus.DoesNotExist:
      # خلي المتغير بغير صحيح
      notifStatus=False
    # الرسالة مش مقروؤه 
    if not notifStatus:
      # زود واحد علي متغير الرسائل غير المقروؤه
      totalUnread +=1
    # طيف بيانات الرسالة في القايمه
    jsonData.append({
      'pk':d.id,
      'not_detail':d.notif_msg,
      'notifStatus':notifStatus
    })
  return render(request,'trainer/notifs.html',{"notifs":jsonData,"totalUnread":totalUnread})




# لتحويل الرسالة الي مقروؤه عند الضغط عليها
def mark_read_trainer_notif(request):
  # متغير تاتي قيمته من اجاكس برقم الرسالة
  notif = request.GET['notif']
  # جلب الرسالة
  notif=models.TrainerNotification.objects.get(pk=notif)
  # جلب اليوزر الحالي
  trainer = models.Trainer.objects.get(id=request.session['trainerid'])
  # انشاء رسالة مقروؤه من اليوزر بمعلوماتها التي حصلنا عليها فوق
  models.NotifTrainerStatus.objects.create(notif=notif,trainer=trainer,status=True)


  # تكرار علي الاشعارات
  totalUnread=0
  data = models.TrainerNotification.objects.all( ).order_by("-id")
  for d in data:
    try:
      # متغير به الرسائل المقروؤه من المستخدم الحالي
      notifStatusData = models.NotifTrainerStatus.objects.get(trainer=trainer,
                notif=d)
      # لو فيه رسائل
      if notifStatusData:
          # خلي المتغير بصح
          notifStatus=True
    # لو مفيش رسائل قرئها اليوزر
    except models.NotifTrainerStatus.DoesNotExist:
      # خلي المتغير بغير صحيح
      notifStatus=False
    # الرسالة مش مقروؤه 
    if not notifStatus:
      # زود واحد علي متغير الرسائل غير المقروؤه
      totalUnread +=1


  # ارسال متغير به صحيح بعد ذالك
  return JsonResponse({'bool':True,'totalUnread':totalUnread})





def trainer_msg(request):
  data = models.TrainerMsg.objects.all( ).order_by("-id")
  return render(request,'trainer/message.html',{"msg":data})





def report_for_user(request):
  trainer = models.Trainer.objects.get(id=request.session['trainerid'])
  if request.POST:
    form=forms.ReportForUserForm(request.POST)
    if form.is_valid():
      new_form=form.save(commit=False)
      new_form.report_from_trainer = trainer
      new_form.save()
      messages.success(request,'Sent Report Successfully..')
      return redirect('trainer_dashboard')
    else:
      messages.warning(request,'Error please try again!!')
      return redirect('report_for_user')
  form = forms.ReportForUserForm
  return render(request,'trainer/report_for_user.html',{'form':form})



def report_for_trainer(request):
  user = request.user
  if request.POST:
    form=forms.ReportForTrainerForm(request.POST)
    if form.is_valid():
      new_form=form.save(commit=False)
      new_form.report_from_user = user
      new_form.save()
      messages.success(request,'Sent Report Successfully..')
      return redirect('trainer_dashboard')
    else:
      messages.warning(request,'Error please try again!!')
      return redirect('report_for_trainer')
  form = forms.ReportForTrainerForm
  return render(request,'user/report_for_trainer.html',{'form':form})



