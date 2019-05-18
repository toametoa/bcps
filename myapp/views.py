from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myapp.models import profile, activities, temps
from myapp.forms import *
from datetime import datetime
from time import gmtime, strftime
import json, os, random
from .mailer import startmailer
from .mailer_spam import startmailer_spam
from .mailfuncs import chartdata, getstat, deltasecs
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator



# Create your views here.
def index(request):

    return render(request, "index.html")



def register(request):
    if request.method == 'POST':
        form =  UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! Your Account Has Been Created! You Can Log In Now!')
            return redirect('login')
    else:
        form =  UserRegisterForm()

    return render(request, "register.html", {'form': form})


@login_required
def uprofile(request):
    currentuser = request.user
    ison = request.user.profile.ison
    isactive = request.user.profile.isactive
    uconfig = profile.objects.get(User=currentuser).uconfig
    ucont = profile.objects.get(User=currentuser).ucont
    webmails = profile.objects.get(User=currentuser).webmails
    econt = profile.objects.get(User=currentuser).econt
    qlistdatas = activities.objects.get(User=currentuser).queuelist
    slistdatas=activities.objects.get(User=currentuser).sentlistlist
    flistdatas=activities.objects.get(User=currentuser).failedlist

    alldates, vallist = chartdata(currentuser)
    mvalue,mvalue2 = getstat(currentuser)


    for key,wmdata in webmails.items():
        print(econt.get(key))
        wmdata['status'] = econt.get(key)


    smaildataset = []
    for key,slistdata in slistdatas.items():
        try:
            sleadmail = slistdata.get('leadmail')
            contdt = ucont.get(sleadmail)
            contdt['time'] = key

            update = slistdata.update(contdt)
            smaildataset = [slistdata] + smaildataset

            asndmail = slistdata.get('asndmail')
            webmail = webmails.get(asndmail)
            webmail['tsent'] = int(webmail['tsent']) +1
        except:
            pass

    qmaildataset = []
    for key,qlistdata in qlistdatas.items():
        qtype = qlistdata.get('mailtype')
        if qtype == 'reply':
            qlistdata.update({'leadmail': key})
            qlistdata.update({'msgno': qlistdata.get('mvalue')})
            qmaildataset = qmaildataset + [qlistdata]
        else:
            qlistdata.update({'leadmail': key})
            qlistdata.update({'msgno': qlistdata.get('mvalue2')})
            qmaildataset = qmaildataset + [qlistdata]

    bcont = profile.objects.get(User=currentuser).bcont
    blacklist = bcont.get('blacklist', [])
    blocked = bcont.get('blocked', [])


    context = { 'alldates':json.dumps(alldates), 'vallist':vallist, 'smaildataset':smaildataset[:40],
    'qmaildataset':qmaildataset[:10],'totalwaiting':len(qmaildataset), "host_con":uconfig['host_con'] , "ison":ison, "momail": uconfig['emaill'], "webmails":webmails, 'ucont':ucont,

    'todaysent':vallist[0], 'totalsent':len(slistdatas), "totalleads": len(ucont),
    "replies": mvalue, "followups": int(mvalue2)-len(ucont), 'totalfailed':len(flistdatas),
    'blacklist':len(blacklist), "blocked": len(blocked),
       }
    return render(request, 'profile.html', context)





class templistview(ListView):
    model = temps
    template_name = 'temps_list.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class templistview2(ListView):
    model = temps
    template_name = 'temps_list2.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class templistview3(ListView):
    model = temps
    template_name = 'temps_list3.html'
    context_object_name = 'posts'
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class tempdetailtview(DetailView):
    model = temps
    template_name = 'temps_det.html'

class tempcreatetview(LoginRequiredMixin, CreateView):
    model = temps
    fields = [ 'subject', 'message', 'delay', 'model_pic_1', 'model_pic_2', 'model_pic_3', 'model_pic_4', 'model_pic_5', 'model_pic_6' ]
    template_name = 'temps_form.html'

class tempupdatetview(LoginRequiredMixin, UpdateView):

    model = temps
    fields = [ 'subject', 'message', 'delay', 'model_pic_1', 'model_pic_2', 'model_pic_3', 'model_pic_4', 'model_pic_5', 'model_pic_6' ]
    template_name = 'temps_form.html'


def sentlist(request):
    ucont = profile.objects.get(User=request.user).ucont
    slistdatas = activities.objects.get(User=request.user).sentlistlist
    smaildataset = []
    for key,slistdata in slistdatas.items():
        try:
            sleadmail = slistdata.get('leadmail')
            contdt = ucont.get(sleadmail)

            update = slistdata.update(contdt)
            smaildataset = [slistdata] + smaildataset
        except:
            pass
    paginator = Paginator(smaildataset,50)
    page = request.GET.get('page')
    smaildataset = paginator.get_page(page)
    context = { 'smaildataset':smaildataset }
    return render(request, "lists/sentlist.html", context)


def waitinglist(request):
    qlistdatas = activities.objects.get(User=request.user).queuelist
    qmaildataset = []
    for key,qlistdata in qlistdatas.items():
        qtype = qlistdata.get('mailtype')
        if qtype == 'reply':
            qlistdata.update({'leadmail': key})
            qlistdata.update({'msgno': qlistdata.get('mvalue')})
            qmaildataset = qmaildataset + [qlistdata]
        else:
            qlistdata.update({'leadmail': key})
            qlistdata.update({'msgno': qlistdata.get('mvalue2')})
            qmaildataset = qmaildataset + [qlistdata]

    paginator = Paginator(qmaildataset,50)
    page = request.GET.get('page')
    qmaildataset = paginator.get_page(page)


    context = { 'qmaildataset':qmaildataset }
    return render(request, "lists/waitinglist.html", context)

def failedlist(request):
    ucont = profile.objects.get(User=request.user).ucont
    flistdatas = activities.objects.get(User=request.user).failedlist
    fmaildataset = []
    for key,flistdata in flistdatas.items():
        try:
            fleadmail = flistdata.get('leadmail')
            contdt = ucont.get(fleadmail)

            update = flistdata.update(contdt)
            fmaildataset = [flistdata] + fmaildataset
        except:
            pass
    paginator = Paginator(fmaildataset,50)
    page = request.GET.get('page')
    fmaildataset = paginator.get_page(page)
    context = { 'fmaildataset':fmaildataset }
    return render(request, "lists/failedlist.html", context)






@login_required
def settings(request):
    currentuser = request.user
    if request.method == 'POST':

        uconfig = profile.objects.get(User=currentuser).uconfig
        uconfig['imap'] = request.POST.get('imap_input', None)
        uconfig['port'] = request.POST.get('port_input', None)
        uconfig['name'] = request.POST.get('name_input', None)
        uconfig['emaill'] = request.POST.get('emaill_input', None)
        uconfig['pass'] = request.POST.get('pass_input', None)
        uconfig['link1'] = request.POST.get('link1_input', None)
        uconfig['link2'] = request.POST.get('link2_input', None)
        profile.objects.filter(User=currentuser).update(uconfig=uconfig)


        context = {"uconfig": uconfig, "fc2":uconfig['imap'], "fc3":uconfig['port'], "fc4":uconfig['name'], "fc5":uconfig['emaill'], "fc6":uconfig['pass'], "fc7":uconfig['link1'], "fc8":uconfig['link2']}
        return redirect('profile')
    else:
        uconfig = profile.objects.get(User=currentuser).uconfig
        context = {"uconfig": uconfig, "fc2":uconfig['imap'],  "fc3":uconfig['port'], "fc4":uconfig['name'], "fc5":uconfig['emaill'], "fc6":uconfig['pass'], "fc7":uconfig['link1'], "fc8":uconfig['link2']}
    return render(request, 'settings.html', context)


def webmail(request,wmlarg):
    currentuser = request.user
    auserdt = profile.objects.get(User=currentuser)
    condta=auserdt.econt
    webmails = profile.objects.get(User=currentuser).webmails
    if request.method == 'POST':
        smtp = request.POST.get('smtp_input', None)
        port = request.POST.get('port_input', None)
        emaill = request.POST.get('emaill_input', None)
        passs = request.POST.get('pass_input', None)
        import smtplib
        try:
            mailServer = smtplib.SMTP(smtp, port)
            mailServer.starttls()
            mailServer.login(emaill, passs)
            mailServer.quit()
            condta[emaill] = 'ok'
            messages.success(request, f'Done! SMTP ACCESS Valid! Successful Login!')
        except Exception as e:
            condta[emaill] = 'notok'
            messages.warning(request, f'Invalid SMTP, Login Failed!')
            pass
        profile.objects.filter(User=currentuser).update(econt=condta)


        dname = request.POST.get('dname_input', None)
        dselctor = request.POST.get('dselctor_input', None)
        dkey = request.POST.get('dkey_input', None)
        gttime = datetime.now()
        addedon = gttime.strftime("%d-%m-%Y")
        if ( smtp != '' and port != '' and emaill != '' and passs != '' ):
            webmails[emaill] = {'smtp':smtp, 'port':port, 'passs':passs, 'addedon':addedon,
            'tsent':0,'dname':dname,'dselctor':dselctor, }
            profile.objects.filter(User=currentuser).update(webmails=webmails)

            # making dir saving pem
            try:
                os.mkdir(os.path.join('/home/metoa/mysite/static/', str(currentuser)))
            except Exception as e:
                print(e, flush = True)
                pass
            pemfile = dselctor+ '.' +dname +'.pem'
            with open("/home/metoa/mysite/static/"+str(currentuser)+"/"+pemfile, 'w+') as file:
                file.write(dkey)
                data = file.read()
                print(data)

            print(dkey)
            messages.success(request, f'Done! SMTP ACCESS Saved!')
            return redirect('profile')
        else:
            messages.warning(request, f'Failed! Please enter valid ACCESS')
            return redirect('profile')
    else:
        if wmlarg in webmails:
            del webmails[wmlarg]
            profile.objects.filter(User=currentuser).update(webmails=webmails)
            messages.success(request, f'Done! Webmail: '+wmlarg+' Deleted!')
            return redirect('profile')

    return render(request, 'addwebmail.html')





def blacklist(request):
    bcont = profile.objects.get(User=request.user).bcont
    blacklist = bcont.get('blacklist', [])
    blocked = bcont.get('blocked', [])
    if len(blacklist) == 0:
        blacklist = ['Blacklist is empty']
    if len(blocked) == 0:
        blocked = [['Nothing Blocked!','00 Minutes ago.']]
    context = { 'blacklist':blacklist,'blocked':blocked, }
    return render(request, "blacklist.html", context)

def blocking(request,adddelarg,mailarg):
    if adddelarg == 'add':
        bcont = profile.objects.get(User=request.user).bcont
        blacklist1 = bcont.get('blacklist', [])
        if mailarg not in blacklist1:
            blacklist1.insert(0, mailarg)
            bcont['blacklist'] = blacklist1
            profile.objects.filter(User=request.user).update(bcont=bcont)
            try:
                qlistdata=activities.objects.get(User=request.user).queuelist
                del qlistdata[mailarg]
                activities.objects.filter(User=request.user).update(queuelist=qlistdata)

            except:
                pass

            messages.success(request, f''+mailarg+' Has Been Added To BlackList!')

    elif adddelarg == 'delete':
        bcont = profile.objects.get(User=request.user).bcont
        blacklist1 = bcont.get('blacklist', [])
        if mailarg in blacklist1:
            blacklist1.remove(mailarg)
            bcont['blacklist'] = blacklist1
            profile.objects.filter(User=request.user).update(bcont=bcont)
            messages.success(request, f''+mailarg+' Has Removed From BlackList!')

    return redirect('blacklist')





def maillist(request):
    currentuser = request.user
    ucont = profile.objects.get(User=currentuser).ucont
    maillist = []
    for mail in ucont:
        rep1 = mail.replace(' ', '' , 1000)
        rep2 = rep1.replace("\r\n", '' , 1000)
        maillist = maillist+[rep2]

    context = {'maillist':maillist,}
    return render(request, "maillist.html", context)

def maillistget(request):
    currentuser = request.user
    if request.method == 'POST':
        webmails = profile.objects.get(User=currentuser).webmails

        mailstr = request.POST.get('mailstr_input', None)
        rep1 = mailstr.replace(' ', '' , 1000)
        rep2 = rep1.replace("\r\n", '' , 1000)
        maillist = list(rep2.split(","))
        gtmvalue = request.POST.get('mvalue_input', None)
        sdtime = request.POST.get('dtime_input', '0')
        dtime = int(sdtime)
        freq=0
        for mail in maillist:
            blacklist = profile.objects.get(User=currentuser).bcont.get('blacklist', [])
            if mail in blacklist:
                bcont = profile.objects.get(User=currentuser).bcont
                blockedl = bcont.get('blocked', [])
                bcont['blocked'] = [[mail, str(datetime.now())]] + blockedl
                profile.objects.filter(User=currentuser).update(bcont=bcont)

            else:

                if type(mail) == str:
                    leadmail = mail
                    firstname = ''
                else:
                    leadmail = mail[0]
                    firstname = mail[1]

                freq +=dtime
                stime = ( datetime.now() + deltasecs(freq))
                if gtmvalue == 'rand':
                    rnd= random.choice([16,17,18,19,20])
                    mvalue =int(rnd)
                else:
                    mvalue = int(gtmvalue)
                asndmail = random.choice(list(webmails.keys()))
                qlistdata=activities.objects.get(User=currentuser).queuelist
                qlistdata[leadmail] = { 'leadmail_mid':'', 'firstname':firstname,
                'stime':str(stime), 'mvalue':mvalue, 'mvalue2':mvalue, 'asndmail':asndmail, 'mailtype':'bulk' }
                activities.objects.filter(User=currentuser).update(queuelist=qlistdata)

                # saveing final lead dataset
                ldataset=profile.objects.get(User=currentuser).ucont
                ldataset[leadmail] = { 'leadmail_mid':'', 'firstname':firstname,
                'stime':str(stime), 'mvalue':1, 'mvalue2':1, 'asndmail':asndmail }
                profile.objects.filter(User=currentuser).update(ucont=ldataset)

        context = { }
        messages.success(request, f'Done! Emails Has Been Pushed To Waiting List!')
        return redirect('profile')
    else:
          context = { }
    return render(request, 'maillistget.html', context)




def on(request):
    currentuser = request.user
    isactive = request.user.profile.isactive
    if isactive == True:
        profile.objects.filter(User=currentuser).update(ison=True)
    else:
        messages.warning(request, f'Can Not Start Autoresponder! Account Is Inactive.')


    return redirect('profile')

def off(request):
    currentuser = request.user
    profile.objects.filter(User=currentuser).update(ison=False)
    profile()

    return redirect('profile')














def start(request):
    startmailer()
    return render(request, "start.html")

def startspam(request):
    startmailer_spam()
    return render(request, "start.html")

# def stop(request):

#     return render(request, "profile.html")
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})



