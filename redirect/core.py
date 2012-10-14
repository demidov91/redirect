from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto.Cipher import AES
from Crypto.Util.randpool import RandomPool

key_generator = RandomPool()

def decrypt_and_select_url(urls, cell, password):    
    """
    cell #0 assumes to be never encrypted
    Method returns dict with 'url' key for result url and 'success' key
     to indicate if it was bad attempt to decrypt some url  
    """
    aes_url = urls[cell]
    aes_url = urlsafe_b64decode(aes_url)
    if cell == 0:
        return {'success':True, 'url':aes_url}
    default_url = urlsafe_b64decode(urls[0])
    try:
        decrypter = AES.new(password)
        return  {'success': True,'url':decrypter.decrypt(aes_url)}
    except (ValueError, TypeError):
        return {'success':False, 'url':default_url}  
    
def encrypt_urls(url_password_pairs):
    """
    `url_password_pairs` - collection of tuples of url and password to encrypt this url
    """
    encrypted_urls = []
    for pair in url_password_pairs:
        if pair[1]:
            encrypter = AES.new(pair[1])
            encrypted_urls.append(encrypter.encrypt(_extend_for_encryption(pair[0])))
        else:
            encrypted_urls.append(pair[0])
    return tuple(urlsafe_b64encode(url) for url in encrypted_urls)

def generate_key(length=16):
    if length % 16:
        raise ValueError('`length` must be a multiple of 16')
    return key_generator.get_bytes(length)

def _extend_for_encryption(original_message):
    """
    'original_message' is human-readable line. Method adds whitespaces to the right of it.
    """
    length_to_be = int(len(original_message) / 16)
    if len(original_message) % 16:
        length_to_be = length_to_be + 1
    return original_message.ljust(length_to_be * 16)




   