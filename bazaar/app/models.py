from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
	tag_name = models.CharField(primary_key=True,max_length = 200)
	def __str__(self):
		return self.tag_name

# Create your models here.
class Profile(models.Model):
	# __entry_years = ['','2010','2011','2012','2013','2014','2015','2016','2017']
	user = models.OneToOneField(User,on_delete=models.DO_NOTHING)
	username=models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	phone=models.IntegerField()
	email=models.CharField(max_length=100,default='xyz@gmail.com')
	image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/user.png')
	followed_tags=models.ManyToManyField(Tag)
	def __str__(self):
		return self.name



class Advertisement(models.Model):
	user = models.ForeignKey(Profile,on_delete=models.DO_NOTHING)
	image = models.ImageField(upload_to = 'ad_pic/', default = 'ad_pic/bat.png')
	title = models.CharField(max_length = 200)
	description = models.CharField(max_length = 500)
	tags=models.ManyToManyField(Tag)
	price = models.FloatField(default=0.0)
	timestamp = models.DateTimeField(auto_now_add=True)
	status=models.IntegerField(default=-1)
	def __str__(self):
		return str(self.id)


class CounterOffer(models.Model):
	ad_id = models.ForeignKey(Advertisement,on_delete=models.DO_NOTHING)
	user_id = models.ForeignKey(Profile,on_delete=models.DO_NOTHING)
	offer = models.FloatField(default=0.0)
	comment=models.CharField(max_length=200)
	def __str__(self):
		return str(self.id)


		