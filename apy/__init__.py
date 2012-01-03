from flask import Flask, request, make_response
from flask.views import MethodView
from werkzeug.exceptions import Unauthorized

import json, re, sys, traceback

from authentication import *
from converters import *
from util import *

__app__ = Flask(__name__)

__app__.always_authenticate = False

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
        return path

    def response(self,output,*args,**kwargs):
        '''Handles permuting the output data based on the supplied params'''
        content_type = kwargs['content_type']
        if content_type == 'json':
            return json.dumps(output)
        elif content_type == 'xml':
            return DictToXML(output)
            #return "<response>XML is not yet supported</response>" % output
        else:
            return output

    def __call__(self,cls):
        '''Wrapper for calling the class'''

        data = self.data
        response = self.response

        class Wrapped(cls,MethodView,object):

            methods = ['get','post','put','delete','head']

            def __init__(self,*args,**kwargs):
                '''Initialize data and http methods'''
                self.data = data
                for method in self.methods: 
                    self.__setattr__(method,self.httpgenerator(method))

            def __getattr__(self,key):  
                '''Attempts to catch any calls to specific http errors and abstract those to the __error__ handler'''
                match = re.search('error_(?P<code>\d+)',key)
                if match: return lambda *args,**kwargs: self.__error__(match.group('code'),*args,**kwargs)
                return data[key]

            def httpgenerator(self,method):
                '''Generator function to pre-define routing of http functions to the __http__ handler'''

                if __app__.always_authenticate:
                    @oauth_protect()
                    def http_response(*args,**kwargs):
                        '''Wrapper to return a HTTP response object'''
                        return self.__http__(method,*args,**kwargs)
                else:
                    
                    def http_response(*args,**kwargs):
                        '''Wrapper to return a HTTP response object'''
                        return self.__http__(method,*args,**kwargs)


                return http_response

            def __http__(self,method,*args,**kwargs):
                '''http request wrapper, returns a proper handler'''

                # Update our kwargs with request args, so they get passed to the higher level handler
                kwargs.update(request.args)
                for k,v in kwargs.iteritems():
                    if type(v) is list and len(v) == 1: kwargs[k] = v[0]

                def handler(env,start_response):
                    '''Actual http handler, uses the response function for the supplied method'''
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
                        return make_response(formatted,200)(env,start_response)
                    except Unauthorized:
                        self.error = 'The credentials you supplied were invalid'
                        return self.error_401(env,start_response)
                    except:
                        return self.error_501(env,start_response)

                return handler

            def __error__(self,code,env,start_response,*args,**kwargs):
                '''Error encountered, start handling the error'''
                data = {
                    'status': code,
                    'message': self.error or 'Server encountered an unknown error'
                }
                return make_response(json.dumps(data),"%s %s" % (code,str(sys.exc_info()[1])))(env,start_response)

        __app__.add_url_rule(self.path, view_func=Wrapped.as_view(cls.__name__))

        return Wrapped

app = __app__
app.url_map.converters['regex'] = RegexConverter