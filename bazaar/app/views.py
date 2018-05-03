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
import requests
import json
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
			if(username == 'Admin'):
				return HttpResponseRedirect('/app/admin/')
			else:	
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
@login_required(login_url='/app/')
def postAd(request):
	assert(request.method == 'POST')
	form = AdForm(request.POST,request.FILES)
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
@login_required(login_url='/app/')
def adForm(request):
	assert(request.method == 'GET')
	adstatus = request.GET.get('adstatus','')
	return render(request, 'adform.html', {'adform':AdForm(),'adstatus':adstatus})

@csrf_exempt
@login_required(login_url='/app/')
def deleteAd(request):
	assert(request.method == 'POST')
	ad_id = request.POST['ad']
	next_ = request.POST.get('next','')
	while next_[-1]=='/':
		next_=next_[:-1]
	try:
		ad=Advertisement.objects.get(id=ad_id)
		offers = CounterOffer.objects.filter(ad_id=ad)
		for offer in offers:
			print("yes")
			Notification.objects.create(ad_id=None,seller=ad.user,buyer=offer.user_id,notify_type=constants.DELETE_AD,read_status=False,meta_data=ad.title)
		ad.delete()

		if next_!='':
			encoding = urllib.parse.urlencode({'delstatus':"Advertisment deleted succesfully"})
			return HttpResponseRedirect(next_+'/?'+encoding)
		else:
			return HttpResponseRedirect('/app/userprofile')

	except Advertisement.DoesNotExist:
		if next_!='':
			encoding = urllib.parse.urlencode({'delstatus':"Advertisment doesn't exist"})
			return HttpResponseRedirect(next_+'/?'+encoding)
		else:
			return HttpResponseRedirect('/app/userprofile')

# @login_required(login_url='/index/')
def tagForm(request):
	assert(request.method == 'GET')
	tagstatus = request.GET.get('tagstatus','')
	return render(request,'addtagform.html',{'addtagform':AddTagForm(),'tagstatus':tagstatus})

@login_required(login_url='/index/')
def addTag(request):
	assert(request.method == 'POST')
	tag_name = request.POST['tag']
	try:
		tag = Tag.objects.get(tag_name=tag_name)
	except Tag.DoesNotExist:
		Tag(tag_name = tag_name).save()
		# encoding = urllib.parse.urlencode({'tagstatus':"Tag added successfully!"})
		return HttpResponseRedirect('/app/admin')
	# encoding = urllib.parse.urlencode({'tagstatus':"Tag already exists!"})
	return HttpResponseRedirect('/app/admin')

@login_required(login_url='/index/')
def removeTagForm(request):
	assert(request.method == 'GET')
	tagstatus = request.GET.get('tagstatus','')
	return render(request,'removetagform.html',{'removetagform':RemoveTagForm(),'tagstatus':tagstatus})

def removeTag(request):
	assert(request.method=='POST')
	tags = [Tag.objects.get(tag_name=tag_id) for tag_id in request.POST.getlist('tags')]
	try:
		for tag in tags:
			ads = Advertisement.objects.filter(tags__tag_name=tag)
			for ad in ads:
				ad.delete()
			tag.delete()
		# encoding = urllib.parse.urlencode({'tagstatus':"Tag deleted successfully!"})
		return HttpResponseRedirect('/app/admin')
	except Tag.DoesNotExist:
		# encoding = urllib.parse.urlencode({'tagstatus':"Tag doesn't exists!"})
		return HttpResponseRedirect('/app/admin')

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

	mybids=mybidlist(profile)
	return render(request, 'userprofile.html', {'profile':profile,'ads':ads,'media_url': MEDIA_URL,'mybids':mybids})

@csrf_exempt
@login_required(login_url='/app/')
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
@login_required(login_url='/app/')
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
@login_required(login_url='/app/')
def bidList(request):
	assert(request.method=='GET')
	ad_id = request.GET.get('ad')
	ad=Advertisement.objects.get(id=ad_id)
	offers=CounterOffer.objects.filter(ad_id=ad_id)
	bids=[]
	for offer in offers:
		bidder=Profile.objects.get(id=offer.user_id.id)
		bid={'bidder':bidder,'comment':offer.comment,'bid':offer.offer,'status':offer.status}	
		bids.append(bid)
	print (bids)
	return render(request,'bidlist.html',{'bids':bids,'ad':ad})


def mybidlist(profile):
	bids=list(CounterOffer.objects.filter(user_id=profile))
	bid_stat=[]
	for bid in bids:
		stat={}
		# ad=Advertisement.objects.get(id=bid.ad_id)
		stat['ad']=bid.ad_id
		stat['bid']=bid
		bid_stat.append(stat)
	return bid_stat

@csrf_exempt
@login_required(login_url='/app/')
def deletebid(request):
	assert(request.method=='POST')
	bid_id=request.POST['bid']
	next_=request.POST.get('next','')
	bidder=Profile.objects.get(user=request.user)
	print(bid_id)
	try:
		co=CounterOffer.objects.get(id=bid_id)
		co.delete()
		return HttpResponseRedirect(next_)
	except CounterOffer.DoesNotExist:
		return HttpResponseRedirect(next_)
	except Advertisement.DoesNotExist:
		return HttpResponseRedirect(next_)



@csrf_exempt
@login_required(login_url='/app/')
def logout_(request):
	logout(request)
	encoding = urllib.parse.urlencode({'loginstatus':"successfully logged out from CampusBazaar"})
	return HttpResponseRedirect('/app/?'+encoding)
	return HttpResponseRedirect('/')


################################### NOTIFICATIONS ##################################

@csrf_exempt
@login_required(login_url='/app/')
def view_notifications(request):
	assert(request.method == 'GET')
	profile = Profile.objects.filter(user=request.user)[0]
	criterion1 = Q(buyer=profile) & (Q(notify_type=constants.ACCEPT_BID) | Q(notify_type=constants.DELETE_AD))
	criterion2 = Q(seller=profile) & (Q(notify_type=constants.UPDATE_BID) | Q(notify_type=constants.NEW_BID) | Q(notify_type=constants.REMOVE_BID))
	result = Notification.objects.filter(criterion1 | criterion2).order_by('-timestamp').distinct()
	notifications = []
	for r in result:
		notify_obj = {'ad_id':r.ad_id,'seller':r.seller,'buyer':r.buyer,
			'notify_type':r.notify_type,'read_status':r.read_status,'timestamp':r.timestamp,'meta_data':r.meta_data}
		if (r.notify_type == constants.UPDATE_BID or r.notify_type == constants.NEW_BID) :
			notify_obj['link_param'] = r.ad_id	
		if (r.notify_type == constants.ACCEPT_BID) :
			notify_obj['link_param'] = r.seller
		if (not(r.read_status)) :
			r.read_status = True
			r.save()
		if (r.notify_type == constants.DELETE_AD) :
			print(r.meta_data)	
		notifications.append(notify_obj)	

	return render(request, 'notifications.html',{'notifications':notifications})

@csrf_exempt
@login_required(login_url='/app/')
def accept_bid(request):
	assert(request.method=='GET')
	ad_id = request.GET.get('ad')
	ad=Advertisement.objects.get(id=ad_id)
	# seller_id = request.POST['seller']
	# seller = Profile.objects.get(id=seller_id)
	bidder_id = request.GET.get('bidder')
	bidder = Profile.objects.get(id=bidder_id)
	Notification.objects.create(ad_id=ad,seller=ad.user,buyer=bidder,
			notify_type=constants.ACCEPT_BID,read_status=False)
	co=CounterOffer.objects.get(ad_id=ad,user_id=bidder)
	co.status = True
	co.save()
	encoding = urllib.parse.urlencode({'ad':ad_id})
	return HttpResponseRedirect('/app/bidlist?'+encoding)
	# return requests.post('/app/bidlist/?', data=json.dumps(payload))

@csrf_exempt
@login_required(login_url='/app/')
def view_seller(request):
	assert(request.method=='GET')
	seller_id = request.GET.get('seller') 
	profile = Profile.objects.get(id=seller_id)
	print()
	return render(request, 'sellerprofile.html', {'profile':profile,'media_url': MEDIA_URL})

@csrf_exempt
@login_required(login_url='/app/')
def admin_control(request):
	assert(request.method=='GET')
	return render(request, 'adminControl.html')