from apy import Endpoint, app

@Endpoint('/main')
class Main:
    '''Basic example returns a json response'''

    def get(*args,**kwargs):
        return {'response': ['hello','world']}

    def post(*args,**kwargs):
        return {'response': ['you','posted']}

app.debug = True
app.run()