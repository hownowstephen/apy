import oauth2, time, urllib2
def build_request(url, method='GET'):
    params = {                                            
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }
    consumer = oauth2.Consumer(key='abc',secret='123')
    params['oauth_consumer_key'] = consumer.key
    print "CONSUMER KEY",consumer.key
 
    req = oauth2.Request(method=method, url=url, parameters=params, body='')
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req

request = build_request('http://localhost:5000/mobs/search?name=yoga')
u = urllib2.urlopen(request.to_url())
print u.readlines()