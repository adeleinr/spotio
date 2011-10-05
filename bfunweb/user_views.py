from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader, RequestContext
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
import urllib, urllib2
from django.utils.functional import curry


from bfunweb.models import UserProfile, Image, ProfileImage
from bfunweb.forms import RegistrationForm, LoginForm, EditUserForm, EditSocialUserForm, ImageForm, ProfileImageForm
from bfunweb.APIConfig import APIConfig

   
def users_index(request):           
  res = urllib.urlopen(APIConfig.USERPROFILE_API_URL)
  users = simplejson.load(res)
  
  return render_to_response('bfunweb/users_index.html',
                            { 'user_list': users},
                            context_instance=RequestContext(request))  


#TODO Need to use API

@login_required(redirect_field_name='bfunweb/login_user')
def user_detail2(request):
    user = request.user
    userProfile = user.get_profile()
     
    #user_count = UserProfile.objects.filter(self_description=userProfile.self_description).count()
   
    similar_users = userProfile.tags.similar_objects()
    

    return render_to_response('bfunweb/user_detail.html',
                              { 'userProfile': userProfile, 
                                'similar_users': similar_users},
                                context_instance=RequestContext(request))

def signup_user(request):
  userForm = RegistrationForm()
  message = ''
  user = request.user
      
  if user is not None and user.is_authenticated():
    return HttpResponseRedirect('/bfunweb/user_detail/'  + user.username)
    
  else:
   
    if request.method == 'POST':
      # Create a form with data to validate form
      testUserForm = RegistrationForm(request.POST)
        
      if testUserForm.is_valid():
        # Use the form data
        try:
          # Save user to db            
          new_user = testUserForm.save()
          
          new_user_profile = UserProfile.objects.create(user=new_user,
                             home_zipcode = request.POST['home_zipcode'])

          user = authenticate(username=request.POST['username'], password=request.POST['password'])
          login(request, user)
          
          return HttpResponseRedirect('/bfunweb/user_detail/')
        except Exception, e:    
                  message = e
      else:
          #User needs to try again
          userForm = testUserForm
          message = 'Invalid form data' 
  
  return render_to_response('bfunweb/signup_user.html', {'message': message, 'userForm': userForm },
        context_instance=RequestContext(request))

def login_user(request):
  
    loginForm = LoginForm()
    message = ''
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          login(request, user)
          # Redirect to a success page
          return HttpResponseRedirect('/bfunweb/user_detail/' + username)
        else:
          message = 'Your account is disabled'
          
      else:
        message = 'Invalid login information'
        
      # Create a form with data to validate form
      testLoginForm = LoginForm(request.POST)
       
  
    return render_to_response('bfunweb/login_user.html', {'loginForm': loginForm, 
                'message':message}, context_instance=RequestContext(request))
  
@login_required(redirect_field_name='bfunweb/login_user')    
def edit_user(request):
  message = ''
  user = request.user
  userProfile = user.get_profile()
  
  if request.facebook:
      editUserForm = EditSocialUserForm(instance = userProfile)
  else:
      editUserForm = EditUserForm(instance = userProfile)
    
     
  if request.method == 'POST':
    
    if 'profileSubmit' in request.POST:
      # Create a form with data to validate form
      if request.facebook:
        editUserForm = EditSocialUserForm(request.POST, instance = userProfile)
      else:
        editUserForm = EditUserForm(request.POST, instance = userProfile)
   
      if editUserForm.is_valid():
          # Use the form data
        try:
          # Save user data
          editUserForm.save()
          
  
        except Exception, e:    
          message = e
      else:
          #User needs to try again)
          message = 'Invalid form data' 
  
  return render_to_response('bfunweb/edit_user.html', {'message': message, 'editUserForm':editUserForm,'userProfile':userProfile },
         context_instance=RequestContext(request))


@login_required(redirect_field_name='bfunweb/login_user')    
def edit_user_picture(request):
  message = ''
  user = request.user
  userProfile = user.get_profile()
        
  ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=1)

  ImageFormSet.form = staticmethod(curry(ProfileImageForm, userProfile))
  
  formset = ImageFormSet(queryset=ProfileImage.objects.none())
         
  if request.method == 'POST':
    
    if request.POST:
      
      formset = ImageFormSet(request.POST,
                             request.FILES,
                             queryset=ProfileImage.objects.none())
      if formset.is_valid():
        instances = formset.save(commit=False)
        for image in instances:
            try:
               image.user = userProfile
               image.save()
               '''
               If not a Social User (Ie. Facebook user) the
               ProfileImage class will upload the image in different
               sizes, so we use the large thumbnail format which is 200x200 pixels
               If a a Social User then his/her picture will
               be pulled from facebook and will be equivalent to this
               200x200 pixels picture
               '''
               # 200x200 pixes
               userProfile.picture_url = image.picture.extra_thumbnails['large'].absolute_url
               userProfile.picture_thumbnail = image.picture.thumbnail.absolute_url
               userProfile.save()
            except ProfileImage.DoesNotExist:
               message = 'does not exit'
      else:
          #User needs to try again)
          message = 'Invalid form data' 
  
  return render_to_response('bfunweb/edit_user_picture.html',
                             {'message': message,
                              'formset':formset,
                              'userProfile':userProfile, },
                             context_instance=RequestContext(request))    

def people_by_tag(request, tag = None):
  
  #tag is a slug
  if tag:
    limit_people = 50
    url = "%s?tag=%s&limit=%d" % (APIConfig.USERPROFILE_API_URL, tag, limit_people)
    res = urllib.urlopen(url)
    people = simplejson.load(res)
    
    return render_to_response('bfunweb/people_by_tag.html',
                                { 'people': people,
                                  'tag': tag},
                                  context_instance=RequestContext(request)) 
  else:
    
    tags = UserProfile.tags.all(); 
    tag_userprofile_map = {}
    limit_people = 10  
    
    for tag in tags:
      url = "%s?tag=%s&limit=%d" % (APIConfig.USERPROFILE_API_URL, tag.slug, limit_people)
      res = urllib.urlopen(url)
      people = simplejson.load(res)
      
      tag_userprofile_map[tag] = people
      
    return render_to_response('bfunweb/people_by_tag.html',
                               { 'tag_userprofile_map': tag_userprofile_map},
                               context_instance=RequestContext(request))                         

