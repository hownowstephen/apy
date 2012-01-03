# Stolen shamelessly from Philip Southam (http://philipsoutham.com/)
import oauth2
from functools import wraps
from flask import Flask, request
from werkzeug.exceptions import Unauthorized
from urlparse import urlparse
import sys
oauth_server = oauth2.Server(signature_methods={
            # Supported signature methods
            'HMAC-SHA1': oauth2.SignatureMethod_HMAC_SHA1()
        })

class MockConsumer(object):
    key = 'ConsumerKey'
    secret = 'ConsumerSecret'
 

def sample_consumer(auth,key):
    '''Example consumer function, generates a MockConsumer'''
    print "Using an unbound mock oAuth consumer - for testing purposes only"
    return MockConsumer()

class oauth_protect():
    '''OAuth decorator'''

    def __init__(self,consumer=None):
        self.consumer = consumer

    def __call__(self,fn,*args,**kwargs):
        def decorated_function(*args, **kwargs):
            self.validate_two_leg_oauth()
            return fn(*args, **kwargs)
        return decorated_function

    def load_consumer(self):
        if self.consumer: 
            return self.consumer
        else: 
            return self.default_consumer

    def validate_two_leg_oauth(self):
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
            consumer = self.load_consumer()
            oauth_server.verify_request(req,
                consumer(request.values.get('oauth_consumer_key')),
                None)
            return True
        except oauth2.Error, e:
            raise Unauthorized(e)
        except:
            print sys.exc_info()
            import traceback
            traceback.print_tb(sys.exc_info()[2])
            raise Unauthorized,"You failed to supply the necessary parameters to properly authenticate"


oauth_protect.default_consumer = sample_consumer
