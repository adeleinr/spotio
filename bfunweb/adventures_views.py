from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils import simplejson
import urllib, urllib2
from decimal import *
from django.utils.functional import curry


from bfunweb.forms import AdventureForm, ImageForm, ProfileImageForm
from bfunweb.models import UserProfile, Adventure, Image, ProfileImage
from bfunweb.APIConfig import APIConfig

'''
============================================================
===================   TOOLBOX VIEWS     ====================
============================================================
'''

def adventure_index(request):

  res = urllib2.urlopen(APIConfig.ADVENTURE_API_URL)
  adventures = simplejson.load(res)
 
  return render_to_response('bfunweb/adventures_index.html',{'adventures': adventures},
                            context_instance=RequestContext(request))
                            
@login_required(redirect_field_name='bfunweb/login_user')
def create_adventure(request):

  message = ''
  user = request.user
  userProfile = user.get_profile()
  
  adventureForm = AdventureForm()

  adventure = Adventure()

  ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)

  ImageFormSet.form = staticmethod(curry(ImageForm, adventure))
          
  formset = ImageFormSet(queryset=Image.objects.none())

  adventure_pictures = ''

    
  if request.method == "POST":
    adventureForm = AdventureForm(request.POST)
    print adventureForm
    if adventureForm.is_valid():
        cost = 0.0
        try:
          adventureForm.user = userProfile
          if request.POST.get('cost'):
            cost = Decimal(request.POST['cost'])

          location_formatted_address = request.POST.get('location_formatted_address')
          location_lat = request.POST.get('location_lat')
          location_lon = request.POST.get('location_lon')

                         
          adventure = Adventure.objects.create(name = request.POST['name'],
                                                 cost =  cost,
                                                 user = userProfile,
                                                 tips = request.POST['tips'],
                                                 location_formatted_address = location_formatted_address,
                                                 location_lat = location_lat,
                                                 location_lon = location_lon)

          ImageFormSet.form = staticmethod(curry(ImageForm, adventure))
          
          formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
          
          if formset.is_valid():
            instances = formset.save(commit=False)
            for image in instances:
              try:
                image.adventure = adventure
                image.save()
                
              except Image.DoesNotExist:
                message = 'Image does not exit'

          message = 'success'

          return HttpResponseRedirect(adventure.get_absolute_url())
            
        except Exception, e:    
          message = e
        # Do something.
    else:
      message = 'Invalid form data'
  
  return render_to_response('bfunweb/create_adventure.html',
                               {'message':message,
                                'adventureForm':adventureForm,
                                'userProfile':userProfile,
                                'formset':formset,
                               }, 
                               context_instance=RequestContext(request))
                               
def adventure_detail(request, adventure_id):
  adventure = get_object_or_404(Adventure, pk=adventure_id)
  picture = adventure.get_picture(1)

  return render_to_response('bfunweb/adventure_detail.html', 
                            {'adventure': adventure, 'picture':picture}, 
                            context_instance=RequestContext(request))

'''

def toolbox_detail(request, toolbox_id):
    res = urllib.urlopen(APIConfig.TOOLBOX_API_URL+str(toolbox_id))
    toolbox = simplejson.load(res)
    return render_to_response('bfunweb/toolbox_detail.html', {'toolbox': toolbox}, 
                              context_instance=RequestContext(request))

def get_newest_toolbox(user):
    try:
        toolbox = ToolBox.objects.filter(user__user__username = user.username).latest()
        return toolbox;
    except: 
        return ''
      


    
@login_required(redirect_field_name='bfunweb/login_user')
def user_toolbox_index(request):
    user = request.user
    userProfile = user.get_profile()
    return render_to_response('bfunweb/user_toolbox_list.html', 
                              {'toolboxes':get_all_toolboxes(userProfile.user.username)},
                              context_instance=RequestContext(request))
'''

'''
@login_required(redirect_field_name='bfunweb/login_user')
def delete_toolbox(request, toolbox_id):
    message = ''
    
    #Get toolbox if it exists
    toolBox = get_object_or_404(ToolBox, pk=toolbox_id)
    
    #Get user from session
    user = request.user
    userProfile = user.get_profile()
    
    #Check that this users owns this toolbox
    if toolBox.user.id ==  userProfile.id:
      userProfile = user.get_profile()  
      opener = urllib2.build_opener(urllib2.HTTPHandler)
      request = urllib2.Request(APIConfig.TOOLBOX_API_URL+str(toolbox_id)+"/")
      request.add_header('Content-Type', 'your/contenttype')
      request.get_method = lambda: 'DELETE'
      url = opener.open(request)

      return HttpResponseRedirect('/bfunweb/user_detail/')

    else:
      #TODO need to show inline error to user
      return HttpResponseRedirect('/bfunweb/user_detail/')

'''



