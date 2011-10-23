from flask import Flask

import json

from authentication import *
from converters import *

__app__ = Flask(__name__)

class endpoint():
    '''Main data endpoint class, manages'''

    def __init__(self,path,auth=None,rate=None,types=['json','xml'],default_type=None):
        '''Initializes the endpoint and sets the target path'''
        self.types = ['\.%s' % t for t in types]
        try:
            if default_type: raise Exception,'Using default_type'
            self.default_type = types[0]
        except:
            self.default_type = default_type

        self.path = self.mutatepath(path)
        self.auth = auth
        self.rate = rate

    def mutatepath(self,base):
        '''Change the path to account for content type'''
        path = '%s<regex("(%s)?"):content_type>' % (base,'|'.join(self.types))
        print "Generated new path descriptor: %s" % path
        return path

    def response(self,output,*args,**kwargs):
        '''Handles permuting the output data based on the supplied params'''
        content_type = kwargs['content_type']
        if content_type == 'json':
            return json.dumps(output)
        elif content_type == 'xml':
            return "<response>XML is not yet supported</response>" % output
        else:
            return output

    def __call__(self,func):
        '''Wrapper for calling the function'''
        @__app__.route(self.path)
        def wrapped(*args,**kwargs):
            output = func(*args,**kwargs)
            # Manage the output content type
            if 'content_type' in kwargs: 
                content_type = kwargs['content_type'].strip('.')
                if not content_type: content_type = self.default_type
                kwargs['content_type'] = content_type
            else:
                kwargs['content_type'] = self.default_type

            return self.response(output,*args,**kwargs)

            
            

        return wrapped


app = __app__
app.url_map.converters['regex'] = RegexConverter