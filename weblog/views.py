# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404 
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from weblog.models import Entry,User,Category,Response
from hashlib import md5
from datetime import datetime

cats=Category.objects.all()
context={'cats':cats}

def liuser(request):
	if 'uname' in request.session:
		return User.objects.get(uname=request.session['uname'])
	return None

def signup(request):
	msg=""
	if 'message' in request.session:
		msg=request.session['message']
		del request.session['message']
	cont={'message':msg}
	new_context=dict(cont.items()+context.items())
	new_context['liuser']=liuser(request)
	return render(request,'signup.html',new_context)

def signup_action(request):
	uname=request.POST['username']
	name=request.POST['name']
	pass1=request.POST['password1']
	pass2=request.POST['password2']
	about=request.POST['about']
	msg=""
	try:
		msg="Username already taken, please choose another"
		user=User.objects.get(uname=uname)	
	except User.DoesNotExist:
		msg=""
	if pass1!=pass2:
		msg="Passwords do not match, try again"
	if pass1=="":
		msg="Password cannot be empty"
	if name=="":
		msg="Name cannot be empty"
	if msg!="":
		request.session['message']=msg
		return HttpResponseRedirect(reverse('signup'))
	
	passhash=md5()
	passhash.update(pass1)
	passh=passhash.hexdigest()
	user=User(uname=uname,name=name,passhash=passh,about=about)
	user.save()
	request.session['message']="Signup successful, login now"
	return HttpResponseRedirect(reverse('index'))

def login(request):
	if 'uname' in request.session:
		request.session['message']="Already Logged in"
		return HttpResponseRedirect(reverse(index))
	msg=""
	if 'message' in request.session:
		msg=request.session['message']
		del	request.session['message']
	cont={'message':msg}
	new_context=dict(cont.items()+context.items())
	new_context['liuser']=liuser(request)
	return render(request,'login.html',new_context)

def login_action(request):
	uname=request.POST['username']
	passh=md5()
	passh.update(request.POST['password'])
	passhash=passh.hexdigest()
	msg=""
	try:
		user=User.objects.get(uname=uname)
	except User.DoesNotExist:
		msg="Username does not exist"
	if msg=="" and user.passhash==passhash:
		request.session['uname']=uname	
		msg="Login Successful"	
		request.session['message']=msg
		return HttpResponseRedirect(reverse('index'))
	else:
		msg="Username/password do not match"
	request.session['message']=msg
	return HttpResponseRedirect(reverse('login'))


def signout(request):
	if 'uname' in request.session:
		del request.session['uname']
	return HttpResponseRedirect(reverse('index'))

def post(request):
	msg=""
	if 'uname' not in request.session:
		msg="You must be logged in to view the page"
	if msg!="":
		request.session["message"]=msg
		return HttpResponseRedirect(reverse('index'))
	new_context=context.copy()
	new_context['liuser']=liuser(request)
	return render(request,'post.html',new_context)

def post_action(request):
	title=request.POST['title']
	content=request.POST['content']
	author=User.objects.get(uname=request.session['uname'])
	date_created=datetime.now()
	category=Category.objects.get(id=request.POST['category'])
	entry=Entry(title=title,content=content,author=author,date_created=date_created,category=category)
	entry.save()
	return HttpResponseRedirect(reverse('index'))

def entry(request,pid):
	msg=""
	try:
		entry=Entry.objects.get(id=pid)
	except Entry.DoesNotExist:
		msg="Entry Not Found!"
		request.session["message"]=msg
	if msg!="":
		return HttpResponseRedirect(reverse('index'))
	
		
	comments=Response.objects.filter(entry=entry)
	
	cont={'entry':entry,'comments':comments}
	new_context=dict(context.items()+cont.items())
	new_context['liuser']=liuser(request)
	return render(request,'entry.html',new_context)

def comment_action(request,pid):
	entry=Entry.objects.get(id=pid)
	responder=User.objects.get(uname=request.session['uname'])
	date=datetime.now()
	response=request.POST['comment']
	comment=Response(entry=entry,responder=responder,date=date,response=response)
	comment.save()
	return HttpResponseRedirect(reverse('entry',kwargs={'pid':pid}))


def index(request,user_id=0,cat_id=0,searchkw=""):
	message=""
	if 'message' in request.session:
		message=request.session['message']
		del request.session['message']
	entries=Entry.objects.all().order_by('-date_created')[:5]
	if user_id!=0:
		try:
			author=User.objects.get(id=user_id)
			entries=Entry.objects.filter(author=author).order_by('-date_created')[:5]
			message="Entries by %s"%author.name
		except User.DoesNotExist:
			message="User does not Exists"
	elif cat_id!=0:
		try:
			cat=Category.objects.get(id=cat_id)
			entries=Entry.objects.filter(category=cat).order_by('-date_created')[:5]
			message="Entries filed in %s"%cat.cname
		except Category.DoesNotExist:
			message="Category does not Exists"
	elif searchkw!="":
		entries=Entry.objects.filter(content__icontains=searchkw)
		message="Search results for %s"%searchkw
			
	cont={'entries':entries,'message':message}
	new_context=dict(context.items()+cont.items())
	new_context['liuser']=liuser(request)
	return render(request,'index.html',new_context)

def search(request):
	searchkw=request.POST["kw"]
	if searchkw=="":
		return HttpResponseRedirect(reverse('index'))
	return HttpResponseRedirect(reverse('index_search',kwargs={'searchkw':searchkw}))

def team(request):
	new_context=context.copy()
	new_context['liuser']=liuser(request)
	return render(request,"team.html",new_context)
