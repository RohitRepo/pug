from random import randint
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required

from .models import User

def site_main(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        context = RequestContext(request)
        return render_to_response("home.html", context)

@login_required
def user_profile(request):
    image_id = randint(50, 999)
    context = RequestContext(request, {'image_id': image_id})
    return render_to_response("profile.html", context)
