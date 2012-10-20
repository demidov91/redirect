from django.http import Http404, HttpResponseRedirect, HttpResponse
import aes
from defines import REDIRECT_TO, URLS_SEPARATOR
from django.template.response import TemplateResponse
from urllib import unquote, quote
from django.template import loader, Context
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta


def redirect_me(request, all_urls):
    try:
        cell = int(request.COOKIES.get('cell', 0))
    except:
        return Http404()
    password = unquote(request.COOKIES.get('password', '')) 
    decrypted_url = _decrypt_and_select_url(all_urls.split(URLS_SEPARATOR), cell, password) 
    if not decrypted_url.startswith('http'):
        decrypted_url = 'http://' + decrypted_url  
    return HttpResponseRedirect(decrypted_url)

def generate(request):
    return TemplateResponse(request, 'generate.html', 
        {
            'host':'http://' + request.META['HTTP_HOST'],
            'cookie_path': COOKIE_PATH,        
        })

def activate(request, cell, password):
    if request.method == 'GET':
        return TemplateResponse(request, 'activate.html')
    response = HttpResponseRedirect(REDIRECT_TO)
    cookie_args = {
        'path':COOKIE_PATH,
        'expires': datetime.now()+timedelta(days=1000),
        }
    response.set_cookie('cell', cell, **cookie_args)
    response.set_cookie('password', quote(password.encode('utf-8')), **cookie_args)
    return response

def clear_cookie(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'delete.html')
    response = HttpResponseRedirect(REDIRECT_TO)
    response.delete_cookie('cell', path=COOKIE_PATH)
    response.delete_cookie('password', path=COOKIE_PATH)
    return response
    

def _decrypt_and_select_url(urls, cell = 0, password = ''):    
    """
    urls - encrypted urls
    cell - index of url to be decrypted. Use 0 as default.
    password - password to decrypt url on the specified position. Use empty string (not None) as default. 
    """
    return aes.decrypt(str(urls[cell]), password, 256)
    
def dummy_404(request):
    raise Http404()

COOKIE_PATH = reverse('redirect_app_root')

