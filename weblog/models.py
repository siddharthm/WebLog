from django.db import models

class User(models.Model):
	uname = models.CharField(max_length=200)
	name= models.CharField(max_length=200)
	
	about = models.TextField()
	passhash=models.CharField(max_length=200)

class Category(models.Model):
	cname = models.CharField(max_length=200)
	description = models.TextField()

class Entry(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(User)
	content = models.TextField()
	category = models.ForeignKey(Category)
	date_created = models.DateTimeField('date published')

class Response(models.Model):
	entry = models.ForeignKey(Entry)
	responder = models.ForeignKey(User)
	date = models.DateTimeField('date of response')
	response = models.TextField()
