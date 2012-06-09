import oauth2, time, urllib2
def build_request(url, method='GET'):
    params = {                                            
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }
    consumer = oauth2.Consumer(key='testkey',secret='testsecret')
    params['oauth_consumer_key'] = consumer.key
 
    req = oauth2.Request(method=method, url=url, parameters=params, body='')
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req

request = build_request('http://dev.tryllo.com:5000/mobs/779003720ee137e/attendees')
u = urllib2.urlopen(request.to_url())
print u.readlines()