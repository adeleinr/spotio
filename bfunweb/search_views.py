from django.template import RequestContext
import haystack
from haystack.indexes import *
from haystack import site
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
import urllib
from bfunweb.APIConfig import APIConfig
from bfunweb.models import Adventure



'''
============================================================
===================   SEARCH VIEWS     ====================
============================================================
'''
def search(request):
  message = ''
  term= ''
  items = []
  url = ''
  if request.method == 'GET':

    term = request.GET.get('q')
    cost = request.GET.get('cost')
    location_formatted_address = request.GET.get('location_formatted_address')
    location_lat = request.GET.get('location_lat')
    location_lon = request.GET.get('location_lon')
    tag = request.POST.get('tag')
    adventure_id = request.GET.get('adventure_id')


  elif request.method == 'POST':
    term = request.POST.get('q')
    cost = request.POST.get('cost')
    location_formatted_address = request.POST.get('location_formatted_address')
    location_lat = request.POST.get('location_lat')
    location_lon = request.POST.get('location_lon')
    tag = request.POST.get('tag')
    adventure_id = request.POST.get('adventure_id')
      
  # If the user left the form blank do nothing
  if not any ([term,cost,location_formatted_address,tag,adventure_id]) :
    return HttpResponseRedirect('/bfunweb/adventures/')


  url = "%s?" % (APIConfig.FULL_SEARCH_API_URL)

  print "In search_view term:" + term
  
  # If have information about the adventure
  # it means the user used the search suggestion
  # to find an adventure that contains it
  # So we retrieve this adventure only
  if adventure_id:
    url = "%s%s" % (APIConfig.TOOLBOX_API_URL, adventure_id)
    res = urllib.urlopen(url)
    items.append(simplejson.load(res))
    
  # else we search for all the adventure names
  else: 
    #TODO Need to change this to urlencode
    if term:
      url = url+"term=%s" % (term)

    if cost:
      url = url+"&cost=%s" % (cost)

    if location_formatted_address:
      url = url+"&location_formatted_address=%s" % (location_formatted_address)

    if tag:
      url = url+"&tag=%s" % (tag)

    print "Calling url:"+url
    res = urllib.urlopen(url)

    print url

    items = simplejson.load(res)
    print "Result: "+str(items);

  return render_to_response('bfunweb/search.html',
                           {'message':message,
                            'adventures':items,
                            'term':term,
                            'cost':cost,
                            'location_formatted_address':location_formatted_address,
                            'location_lat':location_lat,
                            'location_lon':location_lon,
                            'tag':tag,                               
                           }, 
                           context_instance=RequestContext(request))
  #else:     
    #return HttpResponseRedirect('/bfunweb/adventures/')
       
          



  
