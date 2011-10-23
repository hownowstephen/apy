from flask import Flask
from flask.views import MethodView

import json, re

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

            methods = ['get','post','put','delete','head']

            def __init__(self,*args,**kwargs):
                self.data = data
                for method in self.methods: 
                    self.__setattr__(method,self.httpgenerator(method))

            def __getattr__(self,key):  
                match = re.search('error_(?P<code>\d+)',key)
                if match: return lambda *args,**kwargs: self.__error__(match.group('code'),*args,**kwargs)
                return data[key]

            def httpgenerator(self,method):

                def http_response(*args,**kwargs):
                    return self.__http__(method,*args,**kwargs)

                return http_response

            def __http__(self,method,*args,**kwargs):
                
                print "Handling method %s" % method
                def handler(env,start_response,*args,**kwargs):
                    # Manage the output content type
                    if 'content_type' in kwargs: 
                        content_type = kwargs['content_type'].strip('.')
                        if not content_type: content_type = self.default_type
                        kwargs['content_type'] = content_type
                    else:
                        kwargs['content_type'] = self.default_type
                    try:
                        output = getattr(cls,method)(self,*args,**kwargs)
                        formatted = response(output,*args,**kwargs)
                        return start_response(200,[])(formatted)
                    except:
                        return self.error_501(env,start_response)

                return handler

            def __error__(self,code,env,start_response,*args,**kwargs):
                print code,env,start_response
                return start_response(int(code),[])('error')

        __app__.add_url_rule(self.path, view_func=Wrapped.as_view(cls.__name__))

        return Wrapped

app = __app__
app.url_map.converters['regex'] = RegexConverter