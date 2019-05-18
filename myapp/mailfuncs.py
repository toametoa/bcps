from datetime import date, datetime, timedelta
from myapp.models import profile, activities, temps
import random
import uuid

def formattime(strtime):
	return datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f")

def deltaminutes(time):
	return timedelta(minutes=time)
def deltasecs(time):
	return timedelta(seconds=time)


def getmsgdata(auser, msgno):
	udata = temps.objects.filter(user=auser)
	dset = udata[int(msgno)] 
	getmsg = dset.message
	dtime = dset.delay
	subject = dset.subject
	allimages = []
	if dset.model_pic_1:
	    allimages = [dict(title = 'Image 1', path = dset.model_pic_1, cid = str(uuid.uuid4()))] + allimages
	if dset.model_pic_2:
	    allimages = [dict(title = 'Image 2', path = dset.model_pic_2, cid = str(uuid.uuid4()))] + allimages
	if dset.model_pic_3:
	    allimages = [dict(title = 'Image 3', path = dset.model_pic_3, cid = str(uuid.uuid4()))] + allimages
	if dset.model_pic_4:
	    allimages = [dict(title = 'Image 4', path = dset.model_pic_4, cid = str(uuid.uuid4()))] + allimages
	if dset.model_pic_5:
	    allimages = [dict(title = 'Image 5', path = dset.model_pic_5, cid = str(uuid.uuid4()))] + allimages
	if dset.model_pic_6: 
	    allimages = [dict(title = 'Image 6', path = dset.model_pic_6, cid = str(uuid.uuid4()))] + allimages

	return getmsg, dtime, allimages, subject

def repmsg(auser, msg, firstname):
	uconfig = profile.objects.get(User=auser).uconfig

	rep1 = msg.replace('[#username#]', firstname , 10)
	rep2 = rep1.replace('[#modelname#]', uconfig.get('name', '') , 10) 
	rep3 = rep2.replace('[#link1#]', uconfig.get('link1', '') , 10) 
	rep4 = rep3.replace('[#link2#]', uconfig.get('link2', '') , 10) 
	return rep4




def mailproccesor(auser, leadmail , leadmail_mid , firstname , msgtime):
	try:
		rep1 = leadmail.replace(' ', '' , 1000)
		leadmail = rep1.replace("From:", '' , 1000) 
 
		rep1 = firstname.replace(' ', '' , 1000)
		firstname = rep1.replace('"', '' , 1000) 
	except: 
		pass
	blacklist = profile.objects.get(User=auser).bcont.get('blacklist', [])
	if leadmail in blacklist:
		bcont = profile.objects.get(User=auser).bcont
		blockedl = bcont.get('blocked', [])
		bcont['blocked'] = [[leadmail, msgtime]] + blockedl
		profile.objects.filter(User=auser).update(bcont=bcont)
	
	else:
		# get a random webmail
		webmails = profile.objects.get(User=auser).webmails
		randmail = random.choice(list(webmails.keys()))

	    # get or assain mvalue and asnd mail
		msgcount = profile.objects.get(User=auser).ucont
		kvalue = msgcount.get(leadmail, 0)
		if kvalue == 0:
			mvalue = 1
			mvalue2 = 1
			asndmail = randmail
		else:
			mvalue = kvalue.get('mvalue', 1)
			mvalue2 = kvalue.get('mvalue2', 1)
			asndmail = kvalue.get('asndmail', 0)

		checkasndmail = webmails.get(asndmail, 0)
		if checkasndmail == 0:
			asndmail = randmail
		else:
			pass

	      # getting delay time by mvalue
		if mvalue < 11:
			getmsg, dtime, allimages, subject = getmsgdata(auser, int(mvalue) ) 
	        # calculating exact sending time by dtime
			stime = ( msgtime + deltaminutes(dtime))

	        # saveing final lead dataset
			ldataset=profile.objects.get(User=auser).ucont
			ldataset[leadmail] = { 'leadmail_mid':leadmail_mid, 'firstname':firstname, 
			'stime':str(stime), 'mvalue':mvalue, 'mvalue2':mvalue2, 'asndmail':asndmail } 
			profile.objects.filter(User=auser).update(ucont=ldataset)

	        # sending mail and sending time data to queue
			qlistdata=activities.objects.get(User=auser).queuelist
			qlistdata[leadmail] = { 'leadmail_mid':leadmail_mid, 'firstname':firstname, 
			'stime':str(stime), 'mvalue':mvalue, 'mvalue2':mvalue2, 'asndmail':asndmail, 'mailtype':'reply' }
			activities.objects.filter(User=auser).update(queuelist=qlistdata)
		else:
			print(str(auser) + '>>> All 10 Mails Sent to!' + leadmail+ ' Already!(code:- LLA-TNES-RELIAM-201)', flush=True)
			pass

		
	
	
	



def chartdata(user):
	def frmtdate(strtime):
		dtime =  datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f")
		return dtime.strftime("%Y-%m-%d")

	datelist = []
	while len(datelist) < 15:
		newdate = date.today() - timedelta(len(datelist))
		fdate = newdate.strftime('%Y-%m-%d')
		datelist = datelist + [fdate]


	slistdatas=activities.objects.get(User=user).sentlistlist 

	clist = []
	for x in slistdatas:
		y = frmtdate(x) 
		clist = clist +[y] 

	vallist = []
	for adate in datelist:
		tl =  [num for num in clist if num  == adate]
		vallist = vallist + [len(tl)]
		
	alldates = []
	for adate in datelist:
		lk =datetime.strptime(adate, "%Y-%m-%d")
		ll =lk.strftime("%d %b")
		alldates = alldates + [ll]


	return alldates, vallist


def getstat(user):
	ldataset=profile.objects.get(User=user).ucont
	mvalue = 0
	mvalue2 = 0
	for key, ldmail in ldataset.items():
		mvalue = int(mvalue) + int(ldmail['mvalue'])
		mvalue2 = int(mvalue2) + int(ldmail['mvalue2'])
 
	return mvalue,mvalue2