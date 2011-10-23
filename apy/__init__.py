from flask import Flask
from flask.views import MethodView

import json

from authentication import *
from converters import *

__app__ = Flask(__name__)

class Endpoint(object):
    '''Main data endpoint class, manages'''    

    def __init__(self,path,auth=None,rate=None,types=['json','xml'],default_type=None):
        '''Initializes the endpoint and sets the target path'''
        self.data = {}
        self.types = ['\.%s' % t for t in types]
        try:
            if default_type: raise Exception,'Using default_type'
            self.default_type = types[0]
        except:
            self.default_type = default_type

        self.path = self.mutatepath(path)
        self.auth = auth
        self.rate = rate

    def __setattr__(self,key,value):    
        object.__setattr__(self,key,value)
        self.data[key] = value

    def mutatepath(self,base):
        '''Change the path to account for content type'''
        path = '%s<regex("(%s)?"):content_type>' % (base,'|'.join(self.types))
        print "Generated new path descriptor: %s" % path
        return path

    @classmethod
    def response(self,output,*args,**kwargs):
        '''Handles permuting the output data based on the supplied params'''
        content_type = kwargs['content_type']
        if content_type == 'json':
            return json.dumps(output)
        elif content_type == 'xml':
            return "<response>XML is not yet supported</response>" % output
        else:
            return output

    def __call__(self,cls):
        '''Wrapper for calling the class'''

        data = self.data
        response = self.response

        class Wrapped(cls,MethodView,object):

            def __init__(self,*args,**kwargs):
                self.data = data

            def __getattr__(self,key):  
                return data[key]

            def get(self,*args,**kwargs): return self.__http__('get',*args,**kwargs)
            def head(self,*args,**kwargs): return self.__http__('head',*args,**kwargs)
            def post(self,*args,**kwargs): return self.__http__('post',*args,**kwargs)
            def put(self,*args,**kwargs): return self.__http__('put',*args,**kwargs)
            def delete(self,*args,**kwargs): return self.__http__('delete',*args,**kwargs)

            def __http__(self,method,*args,**kwargs):
            
                def handler(env,start_response,*args,**kwargs):
                    # Manage the output content type
                    if 'content_type' in kwargs: 
                        content_type = kwargs['content_type'].strip('.')
                        if not content_type: content_type = self.default_type
                        kwargs['content_type'] = content_type
                    else:
                        kwargs['content_type'] = self.default_type
                    output = getattr(cls,method)(self,*args,**kwargs)
                    formatted = response(output,*args,**kwargs)
                    return start_response(200,[])(formatted)

                return handler

        __app__.add_url_rule(self.path, view_func=Wrapped.as_view(cls.__name__))

        return Wrapped

app = __app__
app.url_map.converters['regex'] = RegexConverter