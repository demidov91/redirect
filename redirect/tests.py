# -*- coding:utf-8 -*-

from django.test import TestCase
from core import encrypt_urls, generate_key, _extend_for_encryption, decrypt_and_select_url
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
        pairs_to_encrypt = (
            ('http://newsbelarus.net/привет/', '1234567890123456'),
            ('https://some url', ''),        
        )
        encrypted = encrypt_urls(pairs_to_encrypt)
        encrypter = AES.new(pairs_to_encrypt[0][1])
        right_answers = (encrypter.encrypt('http://newsbelarus.net/привет/            '), 'https://some url')
        right_answers = tuple(urlsafe_b64encode(url) for url in right_answers)
        self.assertEqual(len(encrypted), 2)
        for compare in zip(right_answers, encrypted):
            self.assertEqual(compare[0], compare[1])
            
class TestDecrypt(TestCase):
    def test_pure_url(self):
        decryption_result = decrypt_and_select_url(('aHR0cDovL25ld3NiZWxhcnVzLm5ldCAgICAgICAgICA=',), 0, None)
        self.assertEqual(decryption_result['success'], True)
        self.assertEqual(decryption_result['url'], 'http://newsbelarus.net          ')
        
    def test_select_pure_url_instead_of_other(self):
        decryption_result = decrypt_and_select_url(('aHR0cDovL25ld3NiZWxhcnVzLm5ldCAgICAgICAgICA=','tU_Sgy-3LHNZkbwAw-Tclg=='), 1, None)
        self.assertEqual(decryption_result['success'], False)
        self.assertEqual(decryption_result['url'], 'http://newsbelarus.net          ')
        
    def test_decrypt_second(self):
        decryption_result = decrypt_and_select_url(('aHR0cDovL25ld3NiZWxhcnVzLm5ldCAgICAgICAgICA=','tU_Sgy-3LHNZkbwAw-Tclg=='), 1, '1234567890123456')
        self.assertEqual(decryption_result['success'], True)
        self.assertEqual(decryption_result['url'], 'tut.by          ')
        