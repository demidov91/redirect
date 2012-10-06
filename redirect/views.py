from django.http import Http404, HttpResponsePermanentRedirect, HttpResponse
from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto.Cipher import AES

def redirect_me(request, *urls):
    if not request.method == 'GET':
        raise Http404()
   
    cell = int(request.COOKIES.get('cell', 0))
    raise Http404()
    aes_url = urls[cell]
    aes_url = urlsafe_b64decode()
    if cell == 0:
        return HttpResponsePermanentRedirect(aes_url)
    password = request.COOKIES.get('password')
    if not password:
        return HttpResponseRedirect(aes_url)
    decrypter = AES.new(password)
    try:
        return  HttpResponseRedirect(decrypter.decrypt(aes_url))
    except:
        return HttpResponseRedirect(aes_url)    



def view_key(request):
    if request.method == 'GET':
        return TemplateResponse('generate_new_key.html')
