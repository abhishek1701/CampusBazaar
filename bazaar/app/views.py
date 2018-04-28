from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from bazaar.settings import MEDIA_ROOT, MEDIA_URL
from app.forms import *
import urllib
from . import constants
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
def tagForm(request):
	assert(request.method == 'GET')
	tagstatus = request.GET.get('tagstatus','')
	return render(request,'addtagform.html',{'addtagform':AddTagForm(),'tagstatus':tagstatus})
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
def removeTagForm(request):
	assert(request.method == 'GET')
	tagstatus = request.GET.get('tagstatus','')
	return render(request,'removetagform.html',{'removetagform':RemoveTagForm(),'tagstatus':tagstatus})

def removeTag(request):
	assert(request.method=='POST')
	tags = [Tag.objects.get(tag_name=tag_id) for tag_id in request.POST.getlist('tags')]
	try:
		for tag in tags:
			tag.delete()
		encoding = urllib.parse.urlencode({'tagstatus':"Tag deleted successfully!"})
		return HttpResponseRedirect('/app/remove_tag_form/?' + encoding)
	except Tag.DoesNotExist:
		encoding = urllib.parse.urlencode({'tagstatus':"Tag doesn't exists!"})
		return HttpResponseRedirect('/app/remove_tag_form/?' + encoding)

def filterAd(filter,profile):
	if(filter=='ALL'):
		return Advertisement.objects.exclude(user=profile)
	else:
		tag=Tag.objects.get(tag_name=filter)
		return Advertisement.objects.filter(tags__tag_name=tag).exclude(user=profile)

@csrf_exempt
@login_required(login_url='/app/')
def feed(request):
	assert(request.method == 'GET')
	tags=list(Tag.objects.all())
	print(tags[0].tag_name)
	profile = Profile.objects.filter(user=request.user)[0]
	ad_filter=request.GET.get('filter','')
	ads=[]
	if(ad_filter==''):
		ads=filterAd('ALL',profile)
	else:
		ads=filterAd(ad_filter,profile)

	# ads =  list(Advertisement.objects.filter(user=profile))
	# ads=filterAd('girl',profile)
	return render(request, 'feed.html', {'tags':tags,'ads':ads,'media_url': MEDIA_URL})


@csrf_exempt
@login_required(login_url='/app/')
def userProfile(request):
	assert(request.method == 'GET')
	profile = Profile.objects.filter(user=request.user)[0]
	Ads =  list(Advertisement.objects.filter(user=profile))
	ads=[]
	for ad in Ads:
		co=list(CounterOffer.objects.filter(ad_id=ad))
		ad_stat={}
		ad_stat['offer_count']=len(co)
		ad_stat['ad']=ad
		ads.append(ad_stat)

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
		#update counter-offer
		co=CounterOffer.objects.get(ad_id=ad,user_id=profile)
		co.offer=bid
		co.comment=comment
		co.save()
		#add notification
		Notification.objects.create(ad_id=ad,seller=ad.user,buyer=profile,notify_type=constants.UPDATE_BID,read_status=False)
		return render(request, 'product.html', {'bidform':BidForm(),'ad':ad,'media_url': MEDIA_URL,'bidstatus':'bid updated successfully'})

	except CounterOffer.DoesNotExist:
		CounterOffer.objects.create(ad_id=ad,user_id=profile,comment=comment,offer=bid)
		#add notification
		Notification.objects.create(ad_id=ad,seller=ad.user,buyer=profile,
			notify_type=constants.NEW_BID,read_status=False)
		return render(request, 'product.html', {'bidform':BidForm(),'ad':ad,'media_url': MEDIA_URL,'bidstatus':'bid added successfully'})


#fetch list of bids for a particular advertisement
@csrf_exempt
def bidList(request):
	assert(request.method=='POST')
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
	return render(request,'bidlist.html',{'bids':bids})


@csrf_exempt
def logout_(request):
	logout(request)
	encoding = urllib.parse.urlencode({'loginstatus':"successfully logout the bazaar"})
	return HttpResponseRedirect('/app/?'+encoding)
	return HttpResponseRedirect('/')


################################### NOTIFICATIONS ##################################

@csrf_exempt
def view_notifications(request):
	user = request.user
	criterion1 = Q(buyer=user) & (Q(notify_type=constants.ACCEPT_BID) | Q(notify_type=constants.DELETE_AD))
	criterion2 = Q(seller=user) & (Q(notify_type=constants.UPDATE_BID) | Q(notify_type=constants.NEW_BID) | Q(notify_type=constants.REMOVE_BID))
	notifications = Notification.objects.filter(criterion1 | criterion2).order_by('-timestamp').distinct()
	for update in notifications:
		if update.read_status :
			break
		else :
			update.read_status = True
			update.save()

		return render(request, 'notifications.html',{'notifications':notifications})
# @csrf_exempt
# def accept_bid(request):
# 	assert(request.method=='POST')
# 	seller = request.user
# 	ad_id = request.
# 	Notification.objects.create(ad_id=ad_id,seller=ad.user,buyer=profile,
# 			notify_type=constants.UPDATE_BID,read_status=false)