from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('redirect.views',
    url(r'to/(?P<all_urls>[a-zA-Z0-9\-_:=]*)/$', 'redirect_me'),
    url(r'to/$', 'dummy_404', name='redirect_start'),
    url(r'create/$', 'generate'),
    url(r'activate/(?P<cell>\d+)/(?P<password>.*)/$', 'activate', name='activate'),
    url(r'activate/$', 'dummy_404', name='activate_start'),
    url(r'clear/', 'clear_cookie', name='clear_cookie'),
    url(r'$', 'dummy_404', name='redirect_app_root'),
)
