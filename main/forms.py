from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from . import models

class EnquiryForm(forms.ModelForm):
  full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name'}), max_length=100)
  email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Addres'}), max_length=100)
  detail = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Your Message'}), max_length=100)
  class Meta:
    model = models.Enquiry
    exclude = ['created_at']



class Signup(UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name','last_name',"username", "email", 'password1', 'password2']


  def __init__(self, *args, **kwargs):
        super(Signup, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class ProfileEdit(UserChangeForm):
  class Meta:
    model = User
    fields = ['first_name','last_name',"username", "email"]



class TrainerLogin(forms.ModelForm):
   class Meta:
      model = models.Trainer
      fields = ['username','pwd']

   def __init__(self, *args, **kwargs):
        super(TrainerLogin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'




class TrainerProfileForm(forms.ModelForm):
   class Meta:
      model = models.Trainer
      fields = [
         'full_name',
         'mobile',
         'address',
         'detail',
         'img',
        ]

   def __init__(self, *args, **kwargs):
        super(TrainerProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'




class TrainerChangePassForm(forms.Form):
    new_pass = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),max_length=100, required=True)


  

class ReportForTrainerForm(forms.ModelForm):

    class Meta:
        model = models.TrainerSubscriberReport
        fields = ('report_for_trainer','report_msg')

    def __init__(self, *args, **kwargs):
        super(ReportForTrainerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ReportForUserForm(forms.ModelForm):

    class Meta:
        model = models.TrainerSubscriberReport
        fields = ('report_for_user','report_msg')

    def __init__(self, *args, **kwargs):
        super(ReportForUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

