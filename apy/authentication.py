# Stolen shamelessly from Philip Southam (http://philipsoutham.com/)
import oauth2
from functools import wraps
from flask import Flask, request
from werkzeug.exceptions import Unauthorized
from urlparse import urlparse
 
oauth_server = oauth2.Server(signature_methods={
            # Supported signature methods
            'HMAC-SHA1': oauth2.SignatureMethod_HMAC_SHA1()
        })

class MockConsumer(object):
    key = 'ConsumerKey'
    secret = 'ConsumerSecret'
 
def _get_consumer(key):
    '''Example consumer function, generates a MockConsumer'''
    print "Using an unbound mock oAuth consumer - for testing purposes only"
    return MockConsumer()
 
def validate_two_leg_oauth(consumer=_get_consumer):
    """
    Verify 2-legged oauth request. Parameters accepted as
    values in "Authorization" header, or as a GET request
    or in a POST body.
    """
    auth_header = {}
    if 'Authorization' in request.headers:
        auth_header = {'Authorization':request.headers['Authorization']}

    parsed = urlparse(request.url)
    uri = "%s://%s%s" % (parsed.scheme,parsed.netloc,parsed.path)

    req = oauth2.Request.from_request(
        request.method,
        uri,
        headers=auth_header,
        # the immutable type of "request.values" prevents us from sending
        # that directly, so instead we have to turn it into a python
        # dict
        parameters=dict([(k,v) for k,v in request.values.iteritems()]))
 
    try:
        oauth_server.verify_request(req,
            consumer(request.values.get('oauth_consumer_key')),
            None)
        return True
    except oauth2.Error, e:
        raise Unauthorized(e)
    except:
        raise Unauthorized,"You failed to supply the necessary parameters to properly authenticate"
 
def oauth_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validate_two_leg_oauth()
        return f(*args, **kwargs)
    return decorated_function
 