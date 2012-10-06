from django.http import Http404, HttpResponsePermanentRedirect, HttpResponse
import json
from core import decrypt_and_select_url
from defines import MAX_ENCODED

def redirect_me(request, *urls):
    try:
        cell = int(request.COOKIES.get('cell', 0))
    except:
        return Http404()
    password = request.COOKIES.get('password')
    return HttpResponsePermanentRedirect(decrypt_and_select_url(urls, cell, password)['url'])
      
def encrypt_json(request, pairs):
    pairs = json.loads(pairs)
    return HttpResponse(json.dumps(encrypt_urls(pairs)), content_type="text/json")


def manage_passwords(request):
    if request.method == 'POST':
        return Http404()
    return TemplateResponse(request, 'generate.html', {'max_encoded_range':range(MAX_ENCODED)})
    
def activate_password(request, cell, password):
    response = HttpResponsePermanentRedirect('http://tut.by')
    response.save_cookie({'cell': cell, 'password':password})
    return response
