from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from django_piston_authentication import DjangoAuthentication
from piston.doc import documentation_view

from api.handlers import UserProfileHandler, AnonymousUserProfileHandler, SearchSuggestionsHandler, SearchHandler, AdventuresHandler, ImagesHandler


#auth = HttpBasicAuthentication(realm='My sample API')

auth = DjangoAuthentication()


#user_profile_resource = Resource(handler=AnonymousUserProfileHandler, authentication=auth) #Resource(AnonymousUserProfileHandler)
user_profile_resource = Resource(handler=AnonymousUserProfileHandler)
'''
tools_resource = Resource(ToolsHandler)
tools_suggestions_resource = Resource(ToolSuggestionsHandler)
'''
search_suggestions_resource = Resource(SearchSuggestionsHandler)
search_resource = Resource(SearchHandler)
adventures_resource = Resource(AdventuresHandler)
images_resource = Resource(ImagesHandler)


urlpatterns = patterns('',
   url(r'^people/$', user_profile_resource, { 'emitter_format': 'json' }),
   url(r'^people/(?P<userprofile_id>\d+)/$', user_profile_resource, { 'emitter_format': 'json' }),
   url(r'^people/(?P<tag>\d+)/$', user_profile_resource, { 'emitter_format': 'json' }),
   url(r'^people/(?P<limit>\d+)/$', user_profile_resource, { 'emitter_format': 'json' }),
   #url(r'^tools/$', tools_resource, { 'emitter_format': 'json' }),
   url(r'^adventures/(?P<adventure_id>\d+)$', adventures_resource, { 'emitter_format': 'ext-json' }),
   url(r'^adventures/$', adventures_resource, {'emitter_format': 'ext-json'}),
   url(r'^images/(?P<adventure_id>\d+)$', images_resource, { 'emitter_format': 'json' }),
   url(r'^images/$', images_resource, { 'emitter_format': 'json' }),
   #url(r'^tool_suggestions/$', tools_suggestions_resource, { 'emitter_format': 'json' }),
   url(r'^search_suggestions/$', search_suggestions_resource, { 'emitter_format': 'ext-json' }),
   url(r'^search/$', search_resource, { 'emitter_format': 'ext-json' }),
   url(r'^doc$', documentation_view),
)
