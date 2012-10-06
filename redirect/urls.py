from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('redirect.views', url(r'(.*?)/(.*?)/(.*?)/$', 'redirect_me'))
