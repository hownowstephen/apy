from apy import Endpoint, app
from apy.authentication import oauth_protect

def some_other_consumer(auth,val):
    print auth,val
    class blah():
        key = 'somekey'
        secret = 'somesecret'
    out =  blah()

    return out

oauth_protect.default_consumer = some_other_consumer



@Endpoint('/main')
class Main:
    '''Basic example returns a json response'''

    def get(*args,**kwargs):
        print args,kwargs
        return {'response': ['hello','world']}

    def post(*args,**kwargs):
        return {'response': ['you','posted']}

    def put(*args,**kwargs):
        return {'response': ['you','put', {'some': 'buttz', 'on': 'toast'}, 'gross']}

    def delete(*args,**kwargs):
        return {'response': {'status': 'success'}}

app.debug = False
app.run()
