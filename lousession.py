#!/usr/bin/env python

import httlib
from urllib import urlencode


_DOMAIN = "www.lordofultima.com"
_URL_LOGIN = "https://%s/en/user/login" % _DOMAIN
_URL_HIDDEN_SESSION_ID = "https://%s/en/game" % _DOMAIN



class Session():

    def __init__(self, mail, password):
        client = httplib2.Http()
        response, content = client.request(_URL_LOGIN,'GET')
        headers = {'Content-type': 'applicationi/x-www-form-urlencoded',
                'Cookie': response['set-cookie']}
        body = dict(mail=mail, password=password)
        response, content = client.request(_URL_LOGIN, 'POST', headers=headers,
                body=urlencode(body))
        headers = {'Cookie': response['set-cookie']}
        response, content = client.request(URL_HIDDEN_SESSION_ID, 'GET'
                headers=headers
        _session = {}
        _session = parse_session_data(content,client)
  

    def parse_session_data(self, contenti, client):
        
        
        
        

