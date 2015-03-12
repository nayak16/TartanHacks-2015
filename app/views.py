"""
Definition of views.
"""

from django.shortcuts import *
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.db.models import F
from app.models import *

# For retreiving email
import apiclient
from apiclient.discovery import build
from apiclient import errors
import httplib2
import logging

import os
import hashlib
import random
import sys
import smtplib
import httplib
import requests
import oauth2client
import gspread
from oauth2client.client import flow_from_clientsecrets


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def new_event(request):
	context = {}
	print request.COOKIES
	
	if 'code' in request.COOKIES:
		context['code'] = request.COOKIES['code']
		print context['code']
	
	return render(request,'app/create_event.html',context)

def redirectBack(request):
	context = {}
	context['hash'] = request.POST['hash']
	return render(request,'app/event_page.html',context)


def log_venmo(request):
	context = {}
	url = request.POST['url']
	tok = request.POST['access_token']	
	amount = request.POST['amount']
	payer = request.POST['payer']
	
	print request.POST
	event_id = request.POST['event_id']
	try:
		event = Event.objects.get(hashString = event_id)
	except:
		return render(request, 'app/404.html')


	user_id = event.admin 

	requests.post('https://api.venmo.com/v1/payments',params={'access_token':tok,'phone':'1'+user_id,'amount':amount,'note':'MoneyPLS Payment for '+event.name})
	#subprocess.call(['curl', 'https://api.venmo.com/v1/payments', '-d', "access_token="+tok,'-d',"phone=1"+user_id,"-d","amount="+amount,"-d","note=moneypls payment"])
	
	event.total= F('total') + float(amount)
	event.contributor_set.create(name=payer, money=float(amount))
	gc = gspread.authorize(event.cred)
	event.save()

# Open a worksheet from spreadsheet with one shot
	sh = gc.open_by_url(event.spread).sheet1
	if len(event.contributor_set.all()) > 0:
		i = 1
		sh.update_acell('A1', 'Person')
		sh.update_acell('B1', 'Money Contributed ($)')
		for c in event.contributor_set.all():
			i+=1
			sh.update_acell('A'+str(i), c.name)
			sh.update_acell('B'+str(i), c.money)

			



	return redirect('/confirmation')

def confirm(request):

	return render(request, 'app/confirmation.html')

def get_user_info(credentials):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except errors.HttpError, e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    return user_info

def create_event(request):
	context = {}

	code = ""
	error = []
	organizer = ""
	name = ""
	admin = ""
	desc = ""
	goal = 0
	total = 0
	end_date = None
	spread = ""
	email = ""
	if 'name' in request.POST:
		name = request.POST['name']
	if 'organizer' in request.POST:
		organizer = request.POST['organizer']
	if 'admin' in request.POST:
		admin = request.POST['admin']
	if 'desc' in request.POST:
		desc = request.POST['desc']
	if 'spread' in request.POST:
		spread = request.POST['spread']
	if 'goal' in request.POST:
		goal = request.POST['goal']
		if(goal == ''):
			goal = 0
	if 'end_date' in request.POST:
		end_date = request.POST['end_date']
	hashS = hashlib.md5(admin + name + str(random.randint(0,sys.maxint))).hexdigest()
	ahashS = hashlib.md5(admin + name + str(random.randint(0,sys.maxint))).hexdigest()



	cred = None
	if 'code' in request.POST:
		code = request.POST['code']
		print "GOOGLE CODE: "+code
		SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
		SCOPES = [
   				'email',
    			'https://www.googleapis.com/auth/calendar',
				]
		flow = flow_from_clientsecrets(SECRETS, ' '.join(SCOPES))
		flow.redirect_uri = 'postmessage'
		cred = flow.step2_exchange(code)

		info = get_user_info(cred)
		email = info['email']



	event = Event(hashString=hashS,adminHashString=ahashS,name=name,organizer=organizer,spread=spread,
					admin=admin,total=total,goal=goal, desc=desc, date=end_date,email=email, cred=cred)
	event.save()
	# Send email to admin
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("moneyplscmu@gmail.com", "gucciswerve")
		msg = "Event Page: http://moneypls.herokuapp.com/event/"+hashS+"\n\nAdmin Page: http://moneypls.herokuapp.com/admin/"+ahashS
		subject = "Event Confirmation for "+name
		message = 'Subject: %s\n\n%s' % (subject, msg)
		server.sendmail("moneyplscmu@gmail.com", email, message)
		server.quit()
	except:
		error.append("Oops something went wrong")


	context['confirm'] = "Success! Check your email for a link to the admin page for the event"
	context['errors'] = error


	return render(request,'app/create_event.html', context)

def admin_event(request, event_id):
	context = {}
	try:
		event = Event.objects.get(adminHashString = event_id)
	except:
		return render(request, 'app/404.html')
	context['hashString'] = event_id
	context['name'] = event.name
	context['admin'] = event.admin
	context['email'] = event.email
	if event.desc != None:
		context['desc'] = event.desc
	if event.goal != None:
		context['goal'] = event.goal
	if event.date != None:
		context['date'] = event.date

	people = []
	if len(event.contributor_set.all()) > 0:
		for c in event.contributor_set.all():
			people.append({'amount':c.money,'name':c.name})
		context['people'] = people
	return render(request, 'app/admin.html', context)

def edit_event(request):
	try:
		event = Event.objects.get(hashString = event_id)
	except:
		return render(request, 'app/404.html')



	context = {}

	return render(request, )

def redirect_event(request):
	context = {}
	context['loggedin'] = True
	event_id = request.GET['state']
	context['access_token'] = request.GET['access_token']
	context['event_id'] = request.GET['state']

	print request.COOKIES
	try:
		event = Event.objects.get(hashString = event_id)
	except:
		return render(request, 'app/404.html')
	context['name'] = event.name
	context['admin'] = event.admin
	context['total'] = event.total
	if event.date != None:
		context['end_date'] = event.date
	if event.desc != None:
		context['desc'] = event.desc
	context['payments'] = len(event.contributor_set.all())
	print event
	if event.goal > 0:
		context['goal'] = event.goal
	people = []
	
	return render(request, "app/event.html", context)


def display_event(request, event_id):
	
	try:
		event = Event.objects.get(hashString = event_id)
	except:
		return render(request, 'app/404.html')

	context = {}
	context['name'] = event.name
	context['admin'] = event.admin
	context['total'] = event.total
	context['organizer'] = event.organizer
	print "THIS"
	print event.organizer
	context['hash'] = event.hashString
	if event.date != None:
		context['end_date'] = event.date
	if event.desc != None:
		context['desc'] = event.desc
	context['payments'] = len(event.contributor_set.all())
	print event
	if event.goal > 0:
		context['goal'] = event.goal
	people = []
	if len(event.contributor_set.all()) > 0:
		for c in event.contributor_set.all():
			people.append({'name':c.name,'amount':c.money})
		context['people'] = people


	return render(request, "app/event.html", context)

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
