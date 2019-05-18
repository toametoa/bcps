from django.contrib.auth.models import User

import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from myapp.models import profile, activities
from datetime import datetime

from .mailfuncs import mailproccesor

def startmailerspam():
	allusers= User.objects.all()
	for auser in allusers:
		auserdt = profile.objects.get(User=auser)
		if auserdt.ison == True and auserdt.isactive == True:
			# getting mailcount(number of new lead msg) by login with mothermail
			try:
				imap_host = auserdt.uconfig['imap']
				host_user = auserdt.uconfig['emaill']
				host_upass = auserdt.uconfig['pass']
				port = auserdt.uconfig['port']
				## open a connection
				mail = imaplib.IMAP4_SSL(imap_host)
				mail.login(host_user, host_upass)
				mail.select("Spam")                                  #select mailbox
				result, data = mail.search(None, "UnSeen")            #search unread "UnSeen"
				mailcount = len(data[0].split())

				print(str(auser) + '>>> Imap Logged In(Spam)', flush=True)
				condta=auserdt.uconfig
				condta['host_con'] = 'ok'
				profile.objects.filter(User=auser).update(uconfig=condta)


				if mailcount == 0:
					print(str(auser) + '>>> No More New Mails!(Spam)', flush=True)
					continue

			except Exception as e:
				print(str(auser) +str(e)+ ' Mothermail Settings PAMI-RELIAM-401)', flush=True)
				mailcount = 0
				condta=auserdt.uconfig
				condta['host_con'] = 'notok'
				profile.objects.filter(User=auser).update(uconfig=condta)
				continue


             # collecting details for every lead, one at a time
			def newmails():                                       #get unread msg mail by calling this function
				global leadmail
				global leadmail_mid
				mail = imaplib.IMAP4_SSL(imap_host)
				mail.login(host_user, host_upass)
				mail.select("Spam")                                  #select mailbox
				result, data = mail.search(None, "UnSeen")            #search unread "UnSeen"
				global mailcount
				mailcount = len(data[0].split())

				ids = data[0]  # data is a list.
				id_list = ids.split()  # ids is a space separated string
				latest_email_id = id_list[-1]  # get the latest

				result, data = mail.fetch(latest_email_id, "(BODY[HEADER.FIELDS (FROM)])")
				raw_email = data[0][1]  # here's the body, which is raw text of the whole email
				raw_strng = raw_email.decode("utf-8")  # decoding byte to str
				leadmail = raw_strng[raw_strng.find("<") + 1:raw_strng.find(">")]  # get exact mail adrss



				result, data2 = mail.fetch(latest_email_id, "(BODY[HEADER.FIELDS (MESSAGE-ID)])")
				raw_mid = data2[0][1]  # here's the body, which is raw text of the whole email
				raw_mid_strng = raw_mid.decode("utf-8")  # decoding byte to str
				leadmail_mid = raw_mid_strng[raw_mid_strng.find("<") + 1:raw_mid_strng.find(">")]  # get exact

				splitted = raw_strng.split()
				firstname = splitted[1]

				msgtime = datetime.now()

                 # sending it to mailfunc m.p. for further proccesing
				mailproccesor(auser, leadmail , leadmail_mid , firstname , msgtime)


			for i in range(mailcount):
				newmails()






def startmailer():
	allusers= User.objects.all()
	for auser in allusers:
		auserdt = profile.objects.get(User=auser)
		if auserdt.ison == True and auserdt.isactive == True:
			# getting mailcount(number of new lead msg) by login with mothermail
			try:
				imap_host = auserdt.uconfig['imap']
				host_user = auserdt.uconfig['emaill']
				host_upass = auserdt.uconfig['pass']
				port = auserdt.uconfig['port']
				## open a connection
				mail = imaplib.IMAP4_SSL(imap_host)
				mail.login(host_user, host_upass)
				mail.select("Inbox")                                  #select mailbox
				result, data = mail.search(None, "UnSeen")            #search unread "UnSeen"
				mailcount = len(data[0].split())

				print(str(auser) + '>>> Imap Logged In(Inbox)', flush=True)
				condta=auserdt.uconfig
				condta['host_con'] = 'ok'
				profile.objects.filter(User=auser).update(uconfig=condta)


				if mailcount == 0:
					print(str(auser) + '>>> No More New Mails!(Inbox)', flush=True)
					pass

			except:
				print(str(auser) + +str(e)+ ' Mothermail Settings PAMI-RELIAM-401)', flush=True)
				mailcount = 0
				condta=auserdt.uconfig
				condta['host_con'] = 'notok'
				profile.objects.filter(User=auser).update(uconfig=condta)
				pass


             # collecting details for every lead, one at a time
			def newmails():                                       #get unread msg mail by calling this function
				global leadmail
				global leadmail_mid
				mail = imaplib.IMAP4_SSL(imap_host)
				mail.login(host_user, host_upass)
				mail.select("inbox")                                  #select mailbox
				result, data = mail.search(None, "UnSeen")            #search unread "UnSeen"
				global mailcount
				mailcount = len(data[0].split())

				ids = data[0]  # data is a list.
				id_list = ids.split()  # ids is a space separated string
				latest_email_id = id_list[-1]  # get the latest

				result, data = mail.fetch(latest_email_id, "(BODY[HEADER.FIELDS (FROM)])")
				raw_email = data[0][1]  # here's the body, which is raw text of the whole email
				raw_strng = raw_email.decode("utf-8")  # decoding byte to str
				leadmail = raw_strng[raw_strng.find("<") + 1:raw_strng.find(">")]  # get exact mail adrss



				result, data2 = mail.fetch(latest_email_id, "(BODY[HEADER.FIELDS (MESSAGE-ID)])")
				raw_mid = data2[0][1]  # here's the body, which is raw text of the whole email
				raw_mid_strng = raw_mid.decode("utf-8")  # decoding byte to str
				leadmail_mid = raw_mid_strng[raw_mid_strng.find("<") + 1:raw_mid_strng.find(">")]  # get exact

				splitted = raw_strng.split()
				firstname = splitted[1]

				msgtime = datetime.now()

                 # sending it to mailfunc m.p. for further proccesing
				mailproccesor(auser, leadmail , leadmail_mid , firstname , msgtime)


			for i in range(mailcount):
				newmails()

			startmailerspam()



