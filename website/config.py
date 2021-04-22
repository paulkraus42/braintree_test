import os
import datetime as dt
import base64
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def base64_encode(string: str) -> str:
    '''
    Encodes the provided byte string into base64
    :param string: A byte string to be encoded. Pass in as b'string to encode'
    :return: a base64 encoded byte string
    '''
    return base64.b64encode(string)


def base64_decode_as_string(bytestring: bytes) -> str:
    '''
    Decodes a base64 encoded byte string into a normal unencoded string
    :param bytestring: The encoded string
    :return: an ascii converted, unencoded string
    '''
    bytestring = base64.b64decode(bytestring)
    return bytestring.decode('ascii')


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'SECRET KEY'
    SECRET_PASSWORD_SALT = 'SECRET SALT'

    MAIL_SERVER = 'smtp-relay.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = False
    MAIL_DEFAULT_SENDER = ('No Reply', 'noreply@host.com')

    ERROR_404_HELP = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ADMIN_EMAILS = ['']


class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    CONFIG_STATE = 'development'
    BRAINTREE_API_URL = 'https://payments.sandbox.braintree-api.com/graphql'
    BRAINTREE_API_KEY_PUB = 'REPLACE'
    BRAINTREE_API_KEY_PRIV = 'REPLACE'
    BRAINTREE_MERCHANT_ID = 'REPLACE'
    BRAINTREE_BASE64 = ('{}:{}'.format(BRAINTREE_API_KEY_PUB ,BRAINTREE_API_KEY_PRIV)).encode('ascii')
    BRAINTREE_BASE64 = base64.b64encode(BRAINTREE_BASE64).decode('ascii')
