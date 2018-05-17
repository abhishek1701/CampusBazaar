from django.core.exceptions import PermissionDenied
from app.models import *
def user_is_admin(function):
    def wrap(request, *args, **kwargs):
    	profile = Profile.objects.filter(user=request.user)[0]
    	print(profile.name)
    	if profile.admin:
    		return function(request, *args, **kwargs)
    	else:
    		return PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap