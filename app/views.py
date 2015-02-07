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

def create_event(request):
	print " created------"
	context = {}
	error = []
	name = ""
	admin = ""
	desc = ""
	goal = 0
	total = 0
	if 'name' in request.POST:
		name = request.POST['name']
	if 'admin' in request.POST:
		admin = request.POST['admin']
	if 'email' in request.POST:
		email = request.POST['email']
	if 'desc' in request.POST:
		desc = request.POST['desc']
	hashS = hashlib.md5(admin + name + str(random.randint(0,sys.maxint))).hexdigest()
	ahashS = hashlib.md5(admin + name + str(random.randint(0,sys.maxint))).hexdigest()
	event = Event(hashString=hashS,adminHashString=ahashS,name=name,
										admin=admin,total=total,goal=goal, desc=desc)
	event.save()
	print event
	# Send email to admin
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("moneyplscmu@gmail.com", "gucciswerve")
		msg = "Event Page: http://moneypls.azurewebsites.net/event/"+hashS+"\n\nAdmin Page: http://moneypls.azurewebsites.net/admin/"+ahashS
		subject = "URL for event "+name
		message = 'Subject: %s\n\n%s' % (subject, msg)
		#server.sendmail("moneyplscmu@gmail.com", email, message)
		server.quit()
	except:
		error.append("Oops something went wrong")


	context['confirm'] = "Success! Check your email for a link to the admin page for the event"
	context['errors'] = error
	return render(request,'app/create_event.html', context)


def display_event(request, event_id):
	
	try:
		event = Event.objects.get(hashString = event_id)
	except:
		return render(request, 'app/404.html')
	context = {}
	context['name'] = event.name
	context['admin'] = event.admin
	context['total'] = event.total
	context['desc'] = event.desc

	print event
	if event.goal > 0:
		context['goal'] = goal
	people = []
	if len(event.contributor_set.all()) > 0:
		for c in event.contributor_set.all():
			people.append({'name':c.name,'amount':c.money})
		context['people'] = people


	return render(request, TODO_CHANGE_THIS, context)

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
