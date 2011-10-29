## Simple, pythonic API development using Flask

Apy provides a high level interface for rapidly prototyping a RESTful API, and deploying on a WSGI-compatible server
Development is done using gunicorn as the base production server, and the flask internal server for testing

API resources are broken into individual endpoints, for which CRUD responses (post,get,put,delete) can be defined as functions
By default both xml and json are supported for endpoints (by adding the .json or .xml suffix) - the default response type is json

Example usage:

```python
from apy import Endpoint

@Endpoint('/main')
class Main:
    '''Basic example returns a json response'''

    def get(*args,**kwargs):
        '''Responds to a GET request'''
        return {'response': 'hello world'}               

    def post(*args,**kwargs):
        '''Responds to a POST request'''
        if not 'name' in kwargs:
            return {'response': 'Please send me your name'}
        else:
            return {'response': 'hello %s' % kwargs['name']}
```