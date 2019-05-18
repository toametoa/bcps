from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from jsonfield import JSONField
from ckeditor.fields import RichTextField
from django.urls import reverse

class  profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    isactive = models.BooleanField(default=False)
    ison = models.BooleanField(default=False)
    uconfig = JSONField(default={ "smtp":"SMTP Is Empty!", "imap":"IMAP Is Empty!", "port":"Port Is Empty!", "emaill":"Email Is Empty!", "pass":"Password Is Empty!", "name":"Name Is Empty!", "host_con":"not ok" , "link1":"example.com" , "link2":"example.com" },blank=True, null=False)
    webmails = JSONField(default={ },blank=True, null=False)
    ucont = JSONField(default={},blank=True, null=False)
    bcont = JSONField(default={"blacklist":[], "blocked":[] },blank=True, null=False)
    econt = JSONField(default={},blank=True, null=False)


    def __str__(self):
    	return str(self.User)

def set_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = profile.objects.create(User=kwargs['instance'])

post_save.connect(set_profile, sender=User)




class  activities(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE,  default='')
    queuelist = JSONField(default={ },blank=True, null=False)
    sentlistlist = JSONField(default={ },blank=True, null=False)
    failedlist = JSONField(default={ },blank=True, null=False)
    elist = JSONField(default={ },blank=True, null=False)
    
    def __str__(self):
        return str(self.User)

def set_activities(sender, **kwargs):
    if kwargs['created']:
        user_profile = activities.objects.create(User=kwargs['instance'])

post_save.connect(set_activities, sender=User)


class temps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    subject = models.CharField(max_length=100,blank=True)
    message = RichTextField(default='Email Template- Is Blank!',blank=True, null=False)
    delay = models.IntegerField(default=456) 
    model_pic_1 = models.ImageField(upload_to = 'Model_pics/',  null=True, blank=True)
    model_pic_2 = models.ImageField(upload_to = 'Model_pics/',  null=True, blank=True)
    model_pic_3 = models.ImageField(upload_to = 'Model_pics/',  null=True, blank=True)
    model_pic_4 = models.ImageField(upload_to = 'Model_pics/',  null=True, blank=True)
    model_pic_5 = models.ImageField(upload_to = 'Model_pics/',  null=True, blank=True)
    model_pic_6 = models.ImageField(upload_to = 'Model_pics/',  null=True, blank=True)
    def __str__(self):
        # return str(self.user)+'---'+str(self.id)
        return str(self.user)+'-'+str(self.id)
    def get_absolute_url(self):
        return reverse('tempdetail', kwargs={'pk': self.pk})

def set_temps(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps, sender=User)

def set_temps1(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps1, sender=User)

def set_temps23(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps23, sender=User)

def set_temps3(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps3, sender=User)
def set_temps4(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps4, sender=User)

def set_temps5(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps5, sender=User)

def set_temps6(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps6, sender=User)

def set_temps7(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps7, sender=User)
def set_temps8(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps8, sender=User)

def set_temps9(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps9, sender=User)

def set_temps10(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps10, sender=User)

def set_temps11(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps11, sender=User)
def set_temps12(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps12, sender=User)

def set_temps13(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps13, sender=User)

def set_temps14(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps14, sender=User)

def set_temps15(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps15, sender=User)
def set_temps16(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps16, sender=User)

def set_temps17(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps17, sender=User)

def set_temps18(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps18, sender=User)

def set_temps19(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps19, sender=User)

def set_temps20(sender, **kwargs):
    if kwargs['created']:
        user_profile = temps.objects.create(user=kwargs['instance'])
post_save.connect(set_temps20, sender=User)

 
