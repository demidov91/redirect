"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from core import encrypt_urls, generate_key, _extend_for_encryption
from base64 import urlsafe_b64encode
from Crypto.Cipher import AES


class TestInternalMethods(TestCase):
    def test_extend_name(self):
        self.assertEqual(len(_extend_for_encryption('http://newsbelarus.net')), 32)


class TestEncrypt(TestCase):
    def test_one_simple(self):
        encrypted = encrypt_urls((('http://newsbelarus.net',''),))
        self.assertEqual(len(encrypted), 1)
        self.assertEqual(encrypted[0], urlsafe_b64encode('http://newsbelarus.net'))
    def test_some_simple(self):
        dict_to_encrypt = (
            ('http://newsbelarus.net',''), 
            ('https://zp',None),
            ('/image/',''),            
        )
        encrypted = encrypt_urls(dict_to_encrypt)
        self.assertEqual(len(encrypted), 3)
        for compare in zip(tuple(pair[0] for pair in dict_to_encrypt), encrypted):
            self.assertEqual(urlsafe_b64encode(compare[0]), compare[1])
    def test_key_generator_default(self):
        self.assertEqual(len(generate_key()), 16)
    def test_key_generator_wrong_length(self):
        self.assertRaises(ValueError, generate_key, 2)
    def test_key_generator_long(self):
        self.assertEqual(len(generate_key(1600)), 1600)
    def test_one_encrypt(self):
        original_url = 'http://newsbelarus.net          '
        password = '0123456789012345'
        encrypted = encrypt_urls(((original_url,password),))
        crypter = AES.new(password)
        self.assertEqual(urlsafe_b64encode(crypter.encrypt(original_url)), encrypted[0])
    def test_some_encrypt(self):
        dict_to_encrypt = (
            ('http://newsbelarus.net','12345678901234567890123456789012'), 
            ('/image/','1234567890123456'),            
        )
        encrypted = encrypt_urls(dict_to_encrypt)
        self.assertEqual(len(encrypted), 2)
        dict_to_encrypt = (
            ('http://newsbelarus.net          ','12345678901234567890123456789012'),
            ('/image/         ','1234567890123456'),
        )
        for compare in zip(dict_to_encrypt, encrypted):
            encrypter = AES.new(compare[0][1])
            self.assertEqual(urlsafe_b64encode(encrypter.encrypt(compare[0][0])), compare[1])
    def test_encrypt_and_simple(self):
        pass