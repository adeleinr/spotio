from django.conf.urls.defaults import *
from bfun.bfunweb import main_views, user_views, adventures_views, proxy_views, search_views
from bfun.bfunweb.models import UserProfile

# General views
urlpatterns = patterns('',
  url(r'^$', main_views.splash),
  url(r'^about/$', main_views.about),
  url(r'^test/$', main_views.test),
)

# User profile related pages
urlpatterns += patterns('',
  url(r'^people/$', user_views.users_index),
  url(r'^user_detail/$', user_views.user_detail2),
  url(r'^signup_user/$', user_views.signup_user),
  url(r'^login_user/$', user_views.login_user),
  url(r'^logout_user/$', 'django.contrib.auth.views.logout_then_login',
      {'login_url':'/bfunweb/login_user'}),
  url(r'^edit_user/$', user_views.edit_user),
  url(r'^edit_user_picture/$', user_views.edit_user_picture),
  url(r'^people_by_tag/(?P<tag>[-\w]+)/$', user_views.people_by_tag),
  url(r'^people_by_tag/$', user_views.people_by_tag),
)

# Adventure related pages
urlpatterns += patterns('',
  url(r'^adventures/$', adventures_views.adventure_index),
  url(r'^create_adventure/$', adventures_views.create_adventure),
  url(r'^adventures/(?P<adventure_id>\d+)/$', adventures_views.adventure_detail), 
  url(r'^search/$', search_views.search), 
)

# Adventure proxies
urlpatterns += patterns('',
  url(r'^proxy/toolbox/$', proxy_views.toolbox),
  url(r'^proxy/adventures/$', proxy_views.adventures),
  url(r'^proxy/search_suggestions/$', proxy_views.search_suggestions)
)
