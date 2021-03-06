from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^signup_form/$', views.signupForm, name='signupForm'),
    url(r'^login/$',views.login_,name='loginURL'),
    url(r'^logout/',views.logout_,name='logoutURL'),
    url(r'^signup/$',views.signup,name='signupURL'),

    url(r'^post_ad/$', views.postAd, name='postAdURL'),
    url(r'^ad_form/$',views.adForm,name='adForm'),
    url(r'^delete_ad/$',views.deleteAd,name='deleteAdURL'),


	url(r'^add_tag/$',views.addTag,name='addtagURL'),
	url(r'^tag_form/',views.tagForm,name='tagFormURL'),
	url(r'^remove_tag/$',views.removeTag,name='removeTagURL'),
	url(r'^remove_tag_form/',views.removeTagForm,name='removeTagFormURL'),

	url(r'^notifications/',views.view_notifications,name='viewNotificationsURL'),
	url(r'^feed/', views.feed,name='feed'),
	url(r'^userprofile/',views.userProfile,name='userProfile'),

	url(r'^product/',views.product,name='productURL'),
	url(r'^bid/',views.bid,name='bidURL'),
	url(r'^bidlist/',views.bidList,name='bidListURL'),
	url(r'^deletebid/',views.deletebid,name='deleteBidURL'),
	
	url(r'^logout/',views.logout_,name='logoutURL'),
	url(r'^accept_bid/',views.accept_bid,name='acceptBidURL'),
	url(r'^admin/',views.admin_control,name='adminControlURL'),
	url(r'^sellerprofile/',views.view_seller,name='sellerProfileURL'),
	# url(r'^filter_ad/',views.filterAd,name='filterAdURL')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
