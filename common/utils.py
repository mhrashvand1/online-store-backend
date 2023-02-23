from urllib import parse
from django.conf import settings
import hashlib

def reverse_dict(dictionary):
    keys = dictionary.keys()
    values = dictionary.values()
    
    if not len(values) == len(set(values)):
        raise ValueError('The dictionary must have unique values so that is it possible to reverse.')
    
    return dict(zip(values, keys))
    

def querystring_to_dict(querystring):
    return parse.parse_qs(querystring)


SECRET_KEY = getattr(settings, "SECRET_KEY")

def hash_string(string):
    string += SECRET_KEY
    sha256 = hashlib.sha256()
    sha256.update(string.encode())
    return sha256.hexdigest()


def send_sms(text, phone_number):
    print(f"{'-'*50}\nSMS sent to {phone_number}\ncontent:\n{text}\n{'-'*50}")
    ...
    # TODO: SMS panel api


def get_abs_url(path):
    main_url = settings.PROJECT_SCHEMA + "://" + settings.PROJECT_HOST + ":" + settings.PROJECT_PORT
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path += '/'
    return main_url + path