#!/usr/bin/env python

import httplib2
from urllib import urlencode
import json

import loumodels
from lousession import Session


#url_ajax = "%sPresentation/Service.svc/ajaxEndpoint/" % (url_main)
#url_server_info = "%sGetServerInfo" % (url_ajax)


content_type = {'content-type':'application/json'}

def get_server_info():
    h = httplib2.Http()
    data = '{"session":"%s"}' % sessionId 
    data = json.dumps({"session": sessionId})
    resp = h.request(url_server_info, "POST", body=data, headers=content_type)
    return resp


if __name__ == "__main__":
    pass


