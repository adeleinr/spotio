from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc
from bfunweb.models import UserProfile
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.utils import simplejson

from bfunweb.models import Adventure, Image
from bfunweb.forms import AdventureForm, ImageForm
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils.functional import curry
from decimal import *

# Used for Search Only
import haystack
from haystack.indexes import *
from haystack.query import SearchQuerySet

# List the users               =>
#      http://localhost:8084/api/people
# Get a user                   =>
#      http://localhost:8084/api/people/1
# Get all users but this one   =>
#      http://localhost:8084/api/people/?exclude=1
# Get users, limit             =>
#      http://localhost:8084/api/people/?limit=3
# Get users, exclude and limit =>
#      http://localhost:8084/api/people/?exclude=1&limit=3
# Get users, tag and limit     =>
#      http://localhost:8084/api/people/?tag=web-dev&limit=3
class UserProfileHandler(BaseHandler):
  allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
  model = UserProfile
  anonymous = 'AnonymousUserProfileHandler'
  fields = ('id', ('user', ('username', 'first_name')),
            'home_zipcode', 'absolute_url','absolute_public_url',
            'picture_url', 'picture_thumbnail', 'tags',)
  
  
  def read(self, request, userprofile_id = None):
    
    if userprofile_id:       
        try:
            userProfile = UserProfile.objects.get(pk = userprofile_id) 
            return userProfile
        except UserProfile.DoesNotExist:
            return rc.NOT_FOUND     
    else:    
      users = []
      if 'exclude' in request.GET:
        # Exclude one user only 
        users = UserProfile.objects.exclude(pk = request.GET['exclude'])
        
      if 'tag' in request.GET:
        users = UserProfile.objects.filter(tags__slug__in=[request.GET['tag']])
    
      if not users:
        # Or get all users   
        users = UserProfile.objects.all()
      
      # Now truncate list if limit specified 
      if 'limit' in request.GET: 
        limit = int(request.GET['limit'])
        users = users[:limit]  
        
      return users
      
  
  @classmethod
  def absolute_url(cls, myinstance):
    return myinstance.get_absolute_url()
  @classmethod
  def absolute_public_url(cls, myinstance):
    return myinstance.get_absolute_public_url()
  
  @classmethod
  def tags(cls, myinstance):
    return myinstance.tags.all()


# List the users  =>
#                 http://localhost:8000/api/people
# Get a user      =>
#                 http://localhost:8000/api/people/1
class AnonymousUserProfileHandler(UserProfileHandler, AnonymousBaseHandler):
  #fields = ('toolbox', 'id', ('user', ('username', 'first_name')),'home_zipcode', 'gender', 'occupation', 'self_description', 'twitter', 'absolute_url')
  fields = ('id', ('user', ('username', 'first_name')),
            'home_zipcode', 'absolute_url', 'absolute_public_url',
            'tags', ('pictures',()), 'picture_url', 'picture_thumbnail')   

  
# Get a search suggestion for 
# a tool or toolbox                   => 
#                   http://localhost:8084/api/search_suggestions/?term=eclipse
# Get a partial suggestion for a tool =>
#                   http://localhost:8084/api/search_suggestions/?term=eclip
class SearchSuggestionsHandler(BaseHandler):
  allowed_methods = ('GET')
    
  def read(self, request):
    response = ""
    term = request.GET['term']
 
    result_list = [] 

    #
    #  To filter more we do something like this:
    #  Eg. results = SearchQuerySet().models(ToolBox, Tool).filter(text__startswith=term).exclude(active=False)

    results = SearchQuerySet().models(Adventure).filter(text__startswith=term)
    #
    #TODO use this limit? 
    #limit = request.GET('limit')  
    #if limit: 
    #    results = results[:int(limit)] 

    item_dict = {}

    for item in results:  
      if(isinstance(item.object, Adventure)):
        item_dict = { 'id': item.object.id , 'value':item.object.name, 'type':'Adventure', 'desc':''}
        
      result_list.append(item_dict)

    return result_list

  
# Search for adventures => 
#                       http://localhost:8084/api/search/?term=carmel
#                       http://localhost:8084/api/search/?cost=100
#                       http://localhost:8084/api/search/term=sf&cost=100&currency_type=USD&location_formatted_address='San Francisco, CA, USA'
class SearchHandler(BaseHandler):
  allowed_methods = ('GET')
  
  def read(self, request):
    response = ""
    result_list = []
    search_results = []

    print request.GET
    
    term = request.GET.get('term')
    cost = request.GET.get('cost')
    location_formatted_address = request.GET.get('location_formatted_address')
    location_lat = request.GET.get('location_lat')
    location_lon = request.GET.get('location_lon')
    
    sqs = SearchQuerySet().models(Adventure);
    
    if term:
      sqs = sqs.filter(text=term)
      
    if cost:     
      sqs = sqs.filter(cost=cost)     
      
    if location_formatted_address:
      sqs = sqs.filter(location_formatted_address=location_formatted_address)

    if location_lat:
      sqs = sqs.filter(location_lat)

    if location_lon:
      sqs = sqs.filter(location_lon)
      
 
    item_dict = {}

    for item in sqs:  
       if (isinstance(item.object, Adventure)):
         result_list.append(get_object_or_404(Adventure, pk=item.object.id))

    return result_list

'''
# List the toolboxes     => http://localhost:8084/api/toolboxes
# Get a toolbox          => http://localhost:8084/api/toolboxes/15
# Get a user's toolboxes => http://localhost:8084/api/toolboxes/adeleinr
# Create a toolbox       => 
# curl -i -X POST -d "toolbox_name=Django%20Tools&tools={%220%22:[%22Eclipse%22,%22/en/eclipse%22],%221%22:[%22Aptana%20IDE%22,%22/en/aptana_ide%22]}&userprofile_id=1" http://localhost:8084/api/toolboxes
#
# curl -i -X POST -H 'Content-Type: application/json' -d '{"toolbox_name": "mytoolbox", "userprofile_id":1, "tools": [{"tool_name": "test1", "note":"my note"},{"tool_name": "test2", "note":"my note"},{"tool_name": "test3", "note":"my note"}]}' http://localhost:8084/api/toolboxes

# Delete a toolbox       => 
#  curl -i -X DELETE  http://localhost:8084/api/toolboxes/14/

# Update a toolbox       =>
# curl -i -X PUT -d "toolbox_name=New name" http://localhost:8084/api/toolboxes/15/    
class ToolboxesHandler(BaseHandler):
  allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
  model = ToolBox
  fields = ('id', 'toolbox_name', 'popularity', 'absolute_url', ('user', ()), ('toolboxtoolrelations', ()),)
  
  def read(self, request, toolbox_id = None, username = None):     
    if toolbox_id:       
        try:
            toolBox = ToolBox.objects.get(pk = toolbox_id) 
            return toolBox
        except ToolBox.DoesNotExist:
            return rc.NOT_FOUND 
    elif username:
        try:
            toolBoxes = ToolBox.objects.filter(user__user__username = username).order_by('-pub_date')
            return toolBoxes
        except Exception:
            return rc.NOT_FOUND 
            
    else:
       return ToolBox.objects.all().order_by('-pub_date')
            
  def create(self, request):
    # This option is for when the input comes
    # structured like in JSON format for example
    if request.content_type:
      
    else:
      userProfile = get_object_or_404(UserProfile, pk=request.POST['userprofile_id'])

      toolBox = ToolBox.objects.create(toolbox_name = request.POST['toolbox_name'],
                                               popularity = 0,
                                               user = userProfile)
      tools = simplejson.loads(request.POST['tools'])
      
      
      # Tools list look like this:
      # [(u'1', [u'Aptana IDE', u'/en/aptana_ide']),
      # (u'0', [u'Eclipse', u'/en/eclipse'])]
      for _, value in tools.items():
        tool_name = value[0]
        tool_semantic_id = value[1]
        
        if not tool_name.isspace() and len(tool_name) > 0:
          try:
            newTool = Tool.objects.get(tool_name=tool_name, tool_semantic_id=tool_semantic_id)
          except: 
            try:
              if tool_name.isspace() or len(tool_name) <= 0:
                tool_semantic_id = 'noid'
              newTool = Tool.objects.create(tool_name=tool_name,tool_semantic_id = tool_semantic_id )
            except Exception, e:
              print e
              return rc.DUPLICATE_ENTRY
                   
            # For now we are just recording that
            # this tool has been used by someone every time
            # TODO: need to remove the active field
            newTool.active = True
            newTool.save()
 
          # toolBox.tools.add(newTool) -> Does not work
          # because we are specifying the 'through' table 
          # Instead we need to create every relation entry
          toolBoxToolRelation = ToolBoxToolRelation.objects.create(toolbox = toolBox,
                                                                  tool= newTool) 
         
      return rc.CREATED


  def delete(self, request, toolbox_id):
    toolbox = ToolBox.objects.get(pk=toolbox_id)
    #TODO
    # print request.user
    # if not request.user == toolbox.user.user:
        return rc.FORBIDDEN # returns HTTP 401
    #
    toolbox.delete()
    
    return rc.DELETED # returns HTTP 204
  
  def update(self, request, toolbox_id):
    toolbox =  toolbox = ToolBox.objects.get(pk=toolbox_id)        
    toolbox.toolbox_name = request.PUT.get('toolbox_name')
    toolbox.save()
    
    return toolbox

    
  @classmethod
  def absolute_url(cls, myinstance):
    return myinstance.get_absolute_url()

'''


# List the adventures     => http://localhost:8084/api/adventures
# Get a adventures        => http://localhost:8084/api/adventures/15
# Get a user's adventures => http://localhost:8084/api/adventures/adeleinr
# Create an adventure     => 
# curl -F "form-0-picture=@/home/adeleinr/Desktop/sandiego_zoo.jpg" -F "name=San Diego Safari" -F "cost=200" -F "userprofile_id=1" -F "tips=" -F "location_formatted_address=San Diego" -F "location_lat=3" -F "location_lon=4"  http://localhost:8084/api/adventures/
#
class AdventuresHandler(BaseHandler):
  allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
  model = Adventure
  fields = ('id', 'name', 'cost', 'picture','big_picture','currency_type','tips','pub_date', 'location_formatted_address','location_lat','location_lon','absolute_url', ('user', ()),)
  
  def read(self, request, adventure_id = None, username = None):     
    if adventure_id:       
        try:
            adventure = Adventure.objects.get(pk = adventure_id) 
            return adventure
        except Adventure.DoesNotExist:
            return rc.NOT_FOUND 
    elif username:
        try:
            adventures = Adventure.objects.filter(user__user__username = username).order_by('-pub_date')
            return adventures
        except Exception:
            return rc.NOT_FOUND 
            
    else:
       return Adventure.objects.all().order_by('-pub_date')

  def create(self, request):
    # This option is for when the input comes
    # structured like in JSON format for example    
    if request.content_type:

      print request

      adventureForm = AdventureForm()
      
      adventure = Adventure()

      ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)

      ImageFormSet.form = staticmethod(curry(ImageForm, adventure))
            
      formset = ImageFormSet(queryset=Image.objects.none())

      adventure_pictures = ''
      
      userProfile = get_object_or_404(UserProfile, pk=request.POST['userprofile_id'])

      #tools = simplejson.loads(request.POST['tools'])

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
              request.POST['form-TOTAL_FORMS']=1
              request.POST['form-INITIAL_FORMS']=0
              
              formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
              
              if formset.is_valid():
                instances = formset.save(commit=False)
                for image in instances:
                  try:
                    image.adventure = adventure
                    image.save()
                    
                  except Image.DoesNotExist:
                    message = 'Image does not exit'
                    return rc.BAD_REQUEST

              else:
                message = "Form is not valid"
                return rc.BAD_REQUEST

          except Exception, e:    
            message = e
            return rc.BAD_REQUEST
               
      return rc.CREATED
          
         
    else:

      return rc.NOT_IMPLEMENTED
      
      
      


  @classmethod
  def picture(cls, myinstance):
    return myinstance.pictures.all()[0].picture.thumbnail

  @classmethod
  def big_picture(cls, myinstance):
    return myinstance.pictures.all()[0].picture.extra_thumbnails['large']

  @classmethod
  def absolute_url(cls, myinstance):
    return myinstance.get_absolute_url()


# List the adventures     => http://localhost:8084/api/images
# Get a adventures        => http://localhost:8084/api/images/15
# Get a user's adventures => http://localhost:8084/api/images/adeleinr
class ImagesHandler(BaseHandler):
  '''
  allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
  model = Image
  fields = ('id','extra_thumbnails_medium','absolute_url', 'adventure',)
  
  def read(self, request, image_id = None, username = None):     
    if image_id:       
        try:
            image = Image.objects.get(pk = image_id) 
            return image
        except Image.DoesNotExist:
            return rc.NOT_FOUND 
    elif username:
        try:
            images = Image.objects.filter(user__user__username = username)
            return images
        except Exception:
            return rc.NOT_FOUND 
            
    else:
       return Image.objects.all()

  # These functions are to expose the fields of the
  # Image.pictures(ImageWithThumbnailsField)
  @classmethod
  def thumbnail(cls, myinstance):
    picture = myinstance.picture.thumbnail  
    return picture
 
  @classmethod
  def extra_thumbnails_medium(cls, myinstance):
    picture = myinstance.picture.extra_thumbnails_tag['medium']  
    return picture

  @classmethod
  def extra_thumbnails_large(cls, myinstance):
    picture = myinstance.picture.extra_thumbnails_tag['large']  
    return picture
  '''
  
