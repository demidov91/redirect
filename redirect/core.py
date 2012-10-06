from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto.Cipher import AES

def decrypt_and_select_url(urls, cell, password):    
    """
    cell #0 assumes to be never encrypted
    Method returns dict with 'url' key for result url and 'success' key
     to indicate if it was bad attempt to decrypt some url  
    """
    aes_url = urls[cell]
    aes_url = urlsafe_b64decode()
    if cell == 0:
        return {'success':True, 'url':aes_url}
    default_url = urlsafe_b64decode(urls[0])
    decrypter = AES.new(password)
    try:
        return  {'sucess': True,'url':decrypter.decrypt(aes_url)}
    except ValueError:
        return {'success':False, 'url':default_url}  
    
def encrypt_urls(url_password_pairs):
    """
    `url_password_pairs` - collection of tuples of url and password to encrypt this url
    """
    encrypted_urls = []
    for pair in url_password_pairs:
        if pair[1]:
            try:
                encrypter = AES.new(pair[1])
                encrypted_urls.append(encrypter.encrypt(extend_for_encryption(pair[0])))
            except ValueError:
                encrypted_urls.append(pair[0])
        else:
            encrypted_urls.append(pair[0])
    return tuple(urlsafe_b64encode(url) for url in encrypted_urls)
            
   