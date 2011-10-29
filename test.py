from apy import Endpoint, app

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

app.debug = True
app.run()