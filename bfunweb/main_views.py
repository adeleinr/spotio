from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from bfunweb.forms import RegistrationForm
from bfunweb.models import UserProfile

def about(request):
  return render_to_response('bfunweb/about.html',
        context_instance=RequestContext(request))


def splash(request):
  return render_to_response('bfunweb/splash.html',
        context_instance=RequestContext(request))

def test(request):
  return render_to_response('bfunweb/test.html',
         context_instance=RequestContext(request))
         
  
