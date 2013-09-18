from django.db import models

class User(models.Model):
	name = models.CharField(max_length=200)
	about = models.TextField()
	access_level = models.IntegerField(default=0) 

class Category(models.Model):
	cname = models.CharField(max_length=200)
	decription = models.TextField()

class Entries(models.Model):
	entry_name = models.CharField(max_length=200)
	author = models.ForeignKey(User)
	summary = models.CharField(max_length=1000)
	content = models.TextField()
	category = models.ForeignKey(Category)
	date_created = models.DateTimeField('date published')

class Responses(models.Model):
	entry = models.ForeignKey(Entries)
	responder = models.ForeignKey(User)
	date = models.DateTimeField('date of response')
	response = models.TextField()
	response_level = models.IntegerField(default=0)
