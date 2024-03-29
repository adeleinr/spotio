from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
import urllib
from bfunweb.APIConfig import APIConfig
   
def toolbox(request):
  data = urllib.urlencode( {'toolbox_name' : request.GET['toolbox_name'],
                            'tools' : request.GET['tools'],
                            'userprofile_id' : request.GET['userprofile_id'] } )
  
  response = urllib.urlopen(APIConfig.TOOLBOX_API_URL, data).read() # HTTP POST Request
  
  return HttpResponse(response)


def adventures(request):
  data = urllib.urlopen(APIConfig.ADVENTURE_API_URL).read() # HTTP GET Request

  # TODO: Read HTTP header from API
  json = simplejson.dumps(data)

  return HttpResponse(json, content_type="application/json")

def search_suggestions(request):
  url = "%s?term=%s" % (APIConfig.SEARCH_API_URL, request.GET['term'])
  result = urllib.urlopen(url).read() # HTTP GET Request

  # TODO: Read HTTP header from API
  return HttpResponse(result, content_type="application/json")
