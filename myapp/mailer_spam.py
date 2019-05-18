
from django.contrib.auth.models import User
import re

import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header
from email.mime.base      import MIMEBase
from email                import encoders

from myapp.models import profile, activities, temps
from .mailfuncs import getmsgdata, repmsg, formattime, deltaminutes
from time import gmtime, strftime
from datetime import datetime
import email, dkim, time, os
import email.header

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext



def startmailer_spam():
	allusers= User.objects.all()
	for auser in allusers:
		auserdt = profile.objects.get(User=auser)
		if auserdt.ison == True and auserdt.isactive == True:
			qlistdatas=activities.objects.get(User=auser).queuelist
			for qlistdata in qlistdatas:
				dataset = qlistdatas.get(qlistdata)
				# calculating current time and sendtime
				stime = dataset.get('stime')
				fdtime = formattime(stime)
				crtime = datetime.now()
				if   fdtime > crtime  :
					print('waiting')
					continue
				else:
					print('sending')


					# getting lead data for sending mail
					try:
						leadmail = qlistdata                              #need
						leadmail_mid = dataset.get('leadmail_mid')        #need
						firstname = dataset.get('firstname')
						mvalue = dataset.get('mvalue')
						mvalue2 = dataset.get('mvalue2')
						asndmail = dataset.get('asndmail')
						mailtype = dataset.get('mailtype')

						# grtting msgno then msg body
						if mailtype == 'followup':
							msgno = int(mvalue2)+10
							mvalue2 += 1
						elif mailtype == 'reply':
							msgno = mvalue
							mvalue += 1
						elif mailtype == 'bulk':
							msgno = mvalue
						# getting dtime(delayTime) and getting formtted msg and replace
						getmsg, dtime, allimages, subject = getmsgdata(auser, int(msgno) )        #need
						body = repmsg(auser, getmsg, firstname)
						textbody = cleanhtml(body)
						# getting mothermail access's
						modelname = auserdt.uconfig.get('name', 0)
						mailaccess = auserdt.webmails.get(asndmail, 0)
						emailll = asndmail                                  #need
						smtp = mailaccess.get('smtp')                       #need
						port = mailaccess.get('port')                       #need
						passs = mailaccess.get('passs')                     #need
						dname = mailaccess.get('dname')
						dselctor = mailaccess.get('dselctor')
						status = 'leadmailok'
					except Exception as e:
						print(e, flush = True)
						status = 'leadmailprob'
						pass


					# sendingdddd;::):):):):):):):):):):):):):):):):):):):
					try:
						def attach_image(img_dict):
							msg_image = MIMEImage(img_dict['path'].read(), name = str(img_dict['path']).split('/')[-1])
							msg_image.add_header('Content-ID', '<{}>'.format(img_dict['cid']))
							return msg_image

						def generate_email(allimages):
							msg =MIMEMultipart('alternative')
							msg['Date'] = email.header.Header( email.utils.formatdate() )
							msg['Subject'] = subject
							msg['From'] = ( '\"' + modelname + '\" ' + '<' + emailll + '>')
							msg['To'] = leadmail
							msg.add_header("Message-ID", email.utils.make_msgid(domain=dname))
							# headers=[ b'Date', b'Subject',b'From', b'To',  b'Message-ID']
							# if leadmail_mid != '':
							msg.add_header('In-Reply-To',  '<' + leadmail_mid + '>' )
							msg.add_header('References',  '<' + leadmail_mid + '>' )

							msg.attach(MIMEText(textbody, 'plain'))
							msg.attach(MIMEText(body, 'html', 'utf-8'))

							for image in allimages:
								msg.attach(attach_image(image))
							try:
								headers=[b'Subject',b'From', b'Date', b'To',  b'Message-ID',b'In-Reply-To',b'References']
								keypath = "/home/metoa/mysite/static/"+str(auser)+"/"
								privateKey = open(os.path.join(keypath, dselctor+'.'+dname+'.pem')).read()
								sig = dkim.sign(msg.as_bytes(), bytes(dselctor,encoding='utf8'), bytes(dname,encoding='utf8'), privateKey.encode(), include_headers=headers)
								sig = sig.decode()
								# Add the DKIM-Signature
								msg['DKIM-Signature'] = sig[len("DKIM-Signature: "):]
							except Exception as e:
								print(e, flush = True)
								pass
							return msg

						def send_email(msg, emailll, passs, port, smtp, leadmail ):
						    mailServer = smtplib.SMTP(smtp, port)
						    mailServer.ehlo()
						    mailServer.starttls()
						    mailServer.ehlo()
						    mailServer.login(emailll, passs)
						    mailServer.sendmail(emailll, leadmail, msg.as_string())
						    mailServer.quit()

						msg = generate_email( allimages)
						send_email(msg, emailll, passs, port, smtp, leadmail )

						status = 'sent'
						condta=auserdt.econt
						condta[emailll] = 'ok'
						profile.objects.filter(User=auser).update(econt=condta)
					except smtplib.SMTPAuthenticationError as er:
					    print(str(auser) +'smtp account error', flush = True)
					    condta=auserdt.econt
					    condta[emailll] = 'notok'
					    profile.objects.filter(User=auser).update(econt=condta)
					except Exception as e:
						print(e, flush = True)
						pass
					# sent done,, now signal followup .......................
					if mvalue2  < 6:
						# calculating exact sending time by dtime
						getmsg, dtime, allimages, subject  = getmsgdata(auser, int(mvalue2)+10 )
						newstime = ( crtime + deltaminutes(dtime))

						# saveing final lead dataset ucont
						ldataset=profile.objects.get(User=auser).ucont
						ldataset[leadmail] = { 'leadmail_mid':leadmail_mid, 'firstname':firstname,
						'stime':str(newstime), 'mvalue':mvalue, 'mvalue2':mvalue2, 'asndmail':asndmail }
						profile.objects.filter(User=auser).update(ucont=ldataset)

						#  new folloup data to queue
						qlistdata=activities.objects.get(User=auser).queuelist
						qlistdata[leadmail] = { 'leadmail_mid':leadmail_mid, 'firstname':firstname,
						'stime':str(newstime), 'mvalue':mvalue, 'mvalue2':mvalue2, 'asndmail':asndmail, 'mailtype':'followup' }
						activities.objects.filter(User=auser).update(queuelist=qlistdata)

					elif mvalue2  > 5:
						print(str(auser) + '>>> All 5 followup Mails Sent to!' + leadmail+ ' Already!(code:- LLA-TNES-RELIAM-201)', flush=True)
						qlistdata=activities.objects.get(User=auser).queuelist
						del qlistdata[leadmail]
						activities.objects.filter(User=auser).update(queuelist=qlistdata)
					else:
						pass



					if status == 'sent':
						if msgno >10:
							msgno = int(msgno)-10
						slistdata=activities.objects.get(User=auser).sentlistlist
						slistdata[str(crtime)] =  { 'leadmail':leadmail, 'senttime':str(crtime),'mailtype':mailtype, 'status':status, 'msgno':msgno}
						activities.objects.filter(User=auser).update(sentlistlist=slistdata)

					elif status == 'leadmailok' or status == 'leadmailprob':
						flistdata=activities.objects.get(User=auser).failedlist
						flistdata[str(crtime)] = { 'leadmail':leadmail, 'mailtype':mailtype, 'status':status, 'msgno':msgno }
						activities.objects.filter(User=auser).update(failedlist=flistdata)
					else:
						pass


