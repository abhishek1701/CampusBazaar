from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Profile, Advertisement, CounterOffer, Tag
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from bazaar.settings import MEDIA_ROOT, MEDIA_URL
from app.forms import *
import urllib

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
MEDIA_URL='/app'+MEDIA_URL


def index(request):
	assert(request.method == 'GET')
	loginstatus = request.GET.get('loginstatus','')
	signupstatus = request.GET.get('signupstatus','')
	next_ = request.GET.get('next','')
	return render(request, 'login.html', {'loginform':AuthenticationForm(),
		'loginstatus':loginstatus,'signupstatus':signupstatus,'next':next_})

@csrf_exempt
def signupForm(request):
	assert(request.method == 'GET')
	loginstatus = request.GET.get('loginstatus','')
	signupstatus = request.GET.get('signupstatus','')
	next_ = request.GET.get('next','')
	return render(request, 'signup.html', {'signupform':SignUpForm(),
		'loginstatus':loginstatus,'signupstatus':signupstatus,'next':next_})

@csrf_exempt
def login_(request):
	assert(request.method == 'POST')
	username = request.POST['username']
	password = request.POST['password']
	next_ = request.POST.get('next','')
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		# return HttpResponse("login successful")
		if(next_==''):
			# profile = Profile.objects.filter(user=user)[0]
			# ads =  list(Advertisement.objects.filter(user=profile))
			# encoding = urllib.parse.urlencode({'ads':ads,'media_url':MEDIA_URL})
			return HttpResponseRedirect('/app/feed/')
			# return render(request, 'feed.html', {'ads':ads,'media_url': MEDIA_URL})
		else:
			return HttpResponseRedirect(next_)
	else:
		encoding = urllib.parse.urlencode({'loginstatus':"Incorrect username/password!",'next':next_})
		return HttpResponseRedirect('/app/?'+encoding)
		# return HttpResponse(encoding)


@csrf_exempt
def signup(request):
	assert(request.method == 'POST')
	form=SignUpForm(request.POST, request.FILES)
	if form.is_valid():
		name = request.POST['name']
		username = request.POST['username']
		password = request.POST['password']
		email=request.POST['email']
		phone=request.POST['phone']
		tags = [Tag.objects.get(tag_name=tag_id) for tag_id in request.POST.getlist('tags')]

		try:
			profile=Profile.objects.get(username=username)
			# user = User.objects.get(username = username)
			# pick different username

		except Profile.DoesNotExist:
			user = User.objects.create_user(username=username, password=password, first_name=name)
			new_profile=Profile.objects.create(user=user,image=request.FILES['image'],username=username,name=name,email=email,phone=phone)
			new_profile.followed_tags.add(*tags)
			# Profile(user=user,name=name).save()
			encoding = urllib.parse.urlencode({'signupstatus':"Signup successful!"})
			return HttpResponseRedirect('/app/signup_form?'+encoding)
	else:
		encoding = urllib.parse.urlencode({'signupstatus':"Invalid form!"})
		return HttpResponseRedirect('/app/signup_form?'+encoding)

# @csrf_exempt
# def postAd(request):
# 	return HttpResponse('hello')

@csrf_exempt
def postAd(request):
	assert(request.method == 'POST')
	form = AdForm(request.POST,request.FILES)
	print(form)
	if form.is_valid():
		title = request.POST['title']
		description=request.POST['description']
		tags = [Tag.objects.get(tag_name=tag_id) for tag_id in request.POST.getlist('tags')]
		user = Profile.objects.filter(user=request.user)[0]
		price=request.POST['price']
		new_ad=Advertisement.objects.create(title=title, description=description,user=user,price=price, image=request.FILES['image'])
		new_ad.tags.add(*tags)
		encoding = urllib.parse.urlencode({'adstatus':"Advertisment added succesfully"})
		return HttpResponseRedirect('/app/ad_form?'+encoding)
	else:
		encoding = urllib.parse.urlencode({'adstatus':"Advertisment not added "})
		return HttpResponseRedirect('/app/ad_form?'+encoding)


@csrf_exempt
# @login_required(login_url='/app/')
def adForm(request):
	assert(request.method == 'GET')
	adstatus = request.GET.get('adstatus','')
	return render(request, 'adform.html', {'adform':AdForm(),'adstatus':adstatus})


# @login_required(login_url='/index/')
def addTag(request):
	assert(request.method == 'POST')
	tag_name = request.POST['tag']
	try:
		tag = Tag.objects.get(tag_name=tag_name)
	except Tag.DoesNotExist:
		Tag(tag_name = tag_name).save()
		encoding = urllib.parse.urlencode({'tagstatus':"Tag added successfully!"})
		return HttpResponseRedirect('/app/tag_form/?' + encoding)
	encoding = urllib.parse.urlencode({'tagstatus':"Tag already exists!"})
	return HttpResponseRedirect('/app/tag_form/?' + encoding)


# @login_required(login_url='/index/')
def tagForm(request):
	assert(request.method == 'GET')
	tagstatus = request.GET.get('tagstatus','')
	return render(request,'addtagform.html',{'addtagform':AddTagForm(),'tagstatus':tagstatus})


@csrf_exempt
@login_required(login_url='/app/')
def feed(request):
	assert(request.method == 'GET')
	profile = Profile.objects.filter(user=request.user)[0]
	ads =  list(Advertisement.objects.filter(user=profile))
	return render(request, 'feed.html', {'ads':ads,'media_url': MEDIA_URL})


@csrf_exempt
@login_required(login_url='/app/')
def userProfile(request):
	assert(request.method == 'GET')
	profile = Profile.objects.filter(user=request.user)[0]
	ads =  list(Advertisement.objects.filter(user=profile))
	return render(request, 'userprofile.html', {'profile':profile,'ads':ads,'media_url': MEDIA_URL})

@csrf_exempt
def product(request):
	assert(request.method=='GET')
	# profile = Profile.objects.filter(user=request.user)[0]
	# ads =  list(Advertisement.objects.filter(user=profile))[0]
	# encoding = urllib.parse.urlencode({'ads':ads})
	bidstatus=request.GET.get('bidstatus','')
	ad_id=request.GET.get('ad','')
	ad=Advertisement.objects.filter(id=ad_id)[0]
	return render(request, 'product.html', {'bidform':BidForm(),'ad':ad,'media_url': MEDIA_URL})


@csrf_exempt
def bid(request):
	assert(request.method=='POST')
	bid = request.POST['bid']
	comment = request.POST['comment']
	ad_id=request.POST['ad']
	ad=Advertisement.objects.get(id=ad_id)
	profile=Profile.objects.get(user=request.user)
	try:
		co=CounterOffer.objects.get(ad_id=ad,user_id=profile)
		co.offer=bid
		co.comment=comment
		co.save()
		return render(request, 'product.html', {'bidform':BidForm(),'ad':ad,'media_url': MEDIA_URL,'bidstatus':'bid updated successfully'})

	except CounterOffer.DoesNotExist:
		CounterOffer.objects.create(ad_id=ad,user_id=profile,comment=comment,offer=bid)
		return render(request, 'product.html', {'bidform':BidForm(),'ad':ad,'media_url': MEDIA_URL,'bidstatus':'bid added successfully'})


@csrf_exempt
def bidList(request):
	assert(request.method=='POST')
	next_ = request.POST['previous']
	ad_id = request.POST['ad']
	# print(next_)
	
	ad=Advertisement.objects.get(id=ad_id)
	offers=CounterOffer.objects.filter(ad_id=ad_id)
	bids=[]
	for offer in offers:
		bidder=Profile.objects.get(id=offer.user_id.id)
		bid={'bidder':bidder.name,'phone':bidder.phone,'comment':offer.comment,'bid':offer.offer}	
		bids.append(bid)
	print (bids)
	return render(request,'bidlist.html',{'bids':bids,'next':next_})



@csrf_exempt
def logout_(request):
	logout(request)
	encoding = urllib.parse.urlencode({'loginstatus':"successfully logout the bazaar"})
	return HttpResponseRedirect('/app/?'+encoding)
	return HttpResponseRedirect('/')



