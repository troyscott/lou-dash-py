#!/usr/bin/env python

from subprocess import Popen, PIPE
import httplib2
from urllib import urlencode
import re

_DOMAIN = "www.lordofultima.com"
_URL_LOGIN = "https://%s/en/user/login" % _DOMAIN
_URL_HIDDEN_SESSION_ID = "https://%s/en/game" % _DOMAIN


class Session():


    def __init__(self, mail, password):
        client = httplib2.Http()
        response, content = client.request(_URL_LOGIN,'GET')
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                'Cookie': response['set-cookie']}
        body = dict(mail=mail, password=password)
        response, content = client.request(_URL_LOGIN, 'POST', headers=headers,
                body=urlencode(body))
        headers = {'Cookie': response['set-cookie']}
        response, content = client.request(_URL_HIDDEN_SESSION_ID, 'GET',
                headers=headers)
        self.session_data = content

    def get_session_id(self):
        find_line = 'name="sessionId" id="sessionId"'
        re_find_value = r".*name=\"sessionId\" id=\"sessionId\" value=\"(.*)\".*"
        return self.parse_session_data(find_line, re_find_value)
       
    def get_game_url(self):
        find_line = 'action="http://prodgame'
        re_find_value = r".*action=\"(.*)\/.*\".*"
        return self.parse_session_data(find_line, re_find_value)
    
    def get_world_id(self):
        find_line = 'value="World ' 
        re_find_value = r".*value=\"(.*)\".*"
        return self.parse_session_data(find_line, re_find_value)
    
    def parse_session_data(self, find_line, re_find_value ):
        data = self.session_data
        p1 = Popen(["echo", data], stdout=PIPE)
        p2 = Popen(["grep", find_line], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        line = p2.communicate()[0]
        pattern = re.compile(re_find_value)
        result = pattern.match(line)
        return result.group(1)
    
