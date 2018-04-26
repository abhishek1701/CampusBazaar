from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^signup_form/$', views.signupForm, name='signupForm'),
    url(r'^login/$',views.login_,name='loginURL'),
    url(r'^signup/$',views.signup,name='signupURL'),
    url(r'^post_ad/$', views.postAd, name='postAdURL'),
    url(r'^ad_form/$',views.adForm,name='adForm'),
	url(r'^add_tag/$',views.addTag,name='addtagURL'),
	url(r'^tag_form/',views.tagForm,name='topicsURL'),
	url(r'^feed/', views.feed,name='feed'),
	url(r'^userprofile/',views.userProfile,name='userProfile'),
	url(r'^product/',views.product,name='productURL'),
	url(r'^bid/',views.bid,name='bidURL'),
	url(r'^bidlist/',views.bidList,name='bidListURL'),
	url(r'^logout/',views.logout_,name='logoutURL')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
