import datetime
import haystack
from haystack.indexes import *
from haystack import site
from bfunweb.models import Adventure

''' 
  should provide a Python import
  path to a file where you keep your
  SearchSite configurations in
'''
haystack.autodiscover()


'''
  Every SearchIndex requires there be one (and only one) field
  with document=True. This indicates to both Haystack and
  the search engine about which field is the primary field
  for searching within.
'''

class AdventureIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True, model_attr='name')
    cost = CharField(model_attr='cost')
    user = CharField(model_attr='user')
    pub_date = DateTimeField(model_attr='pub_date')
    location_formatted_address = CharField(model_attr='location_formatted_address')
    location_lat = CharField(model_attr='location_lat')
    location_lon = CharField(model_attr='location_lon')


    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Adventure.objects.filter(pub_date__lte=datetime.datetime.now())

site.register(Adventure, AdventureIndex)

'''
class ToolBoxIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True, model_attr='toolbox_name')
    user = CharField(model_attr='user')
    pub_date = DateTimeField(model_attr='pub_date')
    
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return ToolBox.objects.filter(pub_date__lte=datetime.datetime.now())
'''
'''     
class ToolIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True, model_attr='tool_name')
    active = BooleanField(model_attr='active')
'''   
'''          
class ToolBoxToolRelationIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True, model_attr='tool.tool_name')
    #tool = CharField(model_attr='tool')
    #toolbox = CharField(model_attr='toolbox')
    
class UserProfileIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True, model_attr='user.get_full_name()')

      
site.register(ToolBox, ToolBoxIndex)
site.register(ToolBoxToolRelation, ToolBoxToolRelationIndex)
'''
      
