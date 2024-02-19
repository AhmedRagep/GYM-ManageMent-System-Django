from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView

def logout_view(request):
    logout(request)
    return redirect('login')


urlpatterns = [
    path('',views.home,name='home'),
    path('page-detail/<int:id>',views.page_detail,name='page-detail'),
    path('faq',views.faq_list,name='faq'),
    path('enquiry',views.enquiry,name='enquiry'),
    path('contact',views.contact_page,name='contact'),
    path('gallery',views.gallery,name='gallery'),
    path('gallery/<int:id>',views.gallery_detail,name='gallery-detail'),
    path('pricing',views.pricing,name='pricing'),
    path('<int:plan_id>/checkout',views.checkout,name='checkout'),
    path('checkout/<int:plan_id>',views.checkout_session,name='checkout_session'),
    path('pay_success',views.pay_success,name='pay_success'),
    path('pay_cancel',views.pay_cancel,name='pay_cancel'),
    

    path('logout',logout_view,name='sign-out'),
    path('signup',views.signup,name='signup'),

    path('user-dashboard',views.dashboard,name='dashboard'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('report-for-trainer',views.report_for_trainer,name='report_for_trainer'),

    path('trainer_login',views.trainer_login,name='trainer_login'),
    path('trainer_logout',views.trainer_logout,name='trainer_logout'),
    path('trainer_dashboard',views.trainer_dashboard,name='trainer_dashboard'),
    path('trainer_profile',views.trainer_profile,name='trainer_profile'),
    path('trainer_subscribers',views.trainer_subscribers,name='trainer_subscribers'),
    path('trainer_payments',views.trainer_payments,name='trainer_payments'),
    path('trainer_changepassword',views.trainer_changepassword,name='trainer_changepassword'),
    path('trainer_notifs',views.trainer_notifs,name='trainer_notifs'),
    path('mark_read_trainer_notif',views.mark_read_trainer_notif,name='mark_read_trainer_notif'),
    path('trainer_msg',views.trainer_msg,name='trainer_msg'),
    path('report-for-user',views.report_for_user,name='report_for_user'),


    path('notifs',views.notifs,name='notifs'),
    path('get_notifs',views.get_notifs,name='get_notifs'),
    path('mark_read_notif',views.mark_read_notif,name='mark_read_notif'),

    path('password_change/',
         PasswordChangeView.as_view(template_name='registration/pass-change.html'),
         name='pass-change'),
]


