from apy import endpoint, app

@endpoint('/main')
def main(*args,**kwargs):
    '''Basic example returns a json response'''
    return {'response': ['hello','world']}

app.debug = True
app.run()