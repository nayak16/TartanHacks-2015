"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import *

import hashlib
import random
import sys
import smtplib
import httplib

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
	return render(request,'app/create_event.html')

def redirect(request):
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
	print user_id

	venmo = httplib.HTTPConnection("api.venmo.com", 80)
	venmo.connect()
	venmo.request('POST', '/v1/payments', 'access_token=%s&user_id=%s&amount=%snote=moneyPLS' % (tok,user_id, amount))
	print venmo.getresponse().read()
	print venmo.getresponse().reason()
	venmo.close()

	
	event.total+=int(amount)
	event.contributor_set.create(name=payer, money=int(amount))


	return render(request, 'app/index.html')

def create_event(request):
	context = {}
	error = []
	name = ""
	admin = ""
	desc = None
	goal = 0
	total = 0
	end_date = None
	email = None
	if 'name' in request.POST:
		name = request.POST['name']
	if 'admin' in request.POST:
		admin = request.POST['admin']
	if 'email' in request.POST:
		email = request.POST['email']
	if 'desc' in request.POST:
		desc = request.POST['desc']
	if 'goal' in request.POST:
		goal = request.POST['goal']
	if 'end_date' in request.POST:
		end_date = request.POST['end_date']
	hashS = hashlib.md5(admin + name + str(random.randint(0,sys.maxint))).hexdigest()
	ahashS = hashlib.md5(admin + name + str(random.randint(0,sys.maxint))).hexdigest()
	event = Event(hashString=hashS,adminHashString=ahashS,name=name,
										admin=admin,total=total,goal=goal, desc=desc, date=end_date,email=email)
	event.save()
	print event
	# Send email to admin
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("moneyplscmu@gmail.com", "gucciswerve")
		msg = "Event Page: http://moneypls.azurewebsites.net/event/"+hashS+"\n\nAdmin Page: http://moneypls.azurewebsites.net/admin/"+ahashS
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
	if len(event.contributor_set.all()) > 0:
		for c in event.contributor_set.all():
			people.append({'name':c.name,'amount':c.money})
		context['people'] = people

	print "========================"
	print context
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
