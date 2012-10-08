#!/usr/bin/env python

import httplib2
from urllib import urlencode
import json

import loumodels
domain = "www.lordofultima.com"
url_login = "https://%s/en/user/login?destination=login" % (domain)
url_start_game = "https://%s/en/game" % (domain)
url_main = "http://prodgame05.lordofultima.com/197/"
url_ajax = "%sPresentation/Service.svc/ajaxEndpoint/" % (url_main)
url_server_info = "%sGetServerInfo" % (url_ajax)

user_mail = ""
user_password = ""

content_type = {'content-type':'application/json'}


def login():
    h = httplib2.Http()
    data = dict(mail=user_mail, password=user_password)
    response, content  = h.request(url_login, 'GET')
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Cookie': response['set-cookie']}
    response, content  = h.request(url_login,'POST', headers=headers, body=urlencode(data))
    headers = {'Cookie': response['set-cookie'] }
    response, content  = h.request(url_start_game, 'GET', headers=headers)
    return content 


def get_server_info():
    h = httplib2.Http()
    data = '{"session":"%s"}' % sessionId 
    data = json.dumps({"session": sessionId})
    resp = h.request(url_server_info, "POST", body=data, headers=content_type)
    return resp


if __name__ == "__main__":
    print 'Test login'
    print login()
    #print get_server_info()

