#!/usr/bin/env python

from subprocess import Popen, PIPE
import httplib2
from urllib import urlencode
import re

_DOMAIN = "www.lordofultima.com"
_URL_LOGIN = "https://%s/en/user/login" % _DOMAIN
_URL_HIDDEN_SESSION_ID = "https://%s/en/game" % _DOMAIN


class Session():
    """Creates a new Session for the Lord of Ultima Game
    
    Given a valid username (e-mail address)  and password the system
    logs into the Lord of Ultima server and retrieves the necessary
    session_id which is used for the JSON API requests.

    Attributes:
        session_id: Lord of Ultima Session Id (Cookie)
        world_id: Name of World
        game_url: URL for the current game.

    """
    #TODO: Add errorhandling for invalid logon/connection errors
    def __init__(self, mail, password):
        client = httplib2.Http()
        response, content = client.request(_URL_LOGIN,'GET')
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                'Cookie': response['set-cookie']}
        body = dict(mail=mail, password=password)
        response, content = client.request(_URL_LOGIN, 'POST', headers=headers,
                body=urlencode(body))
        print 'Response login: %s' % response
        headers = {'Cookie': response['set-cookie']}
        response, content = client.request(_URL_HIDDEN_SESSION_ID, 'GET',
                headers=headers)
        self.session_data = content
        self.session_id = self.__get_session_id()
        self.game_url = self.__get_game_url()
        self.world_id = self.__get_world_id()

    def __get_session_id(self):
        find_line = 'name="sessionId" id="sessionId"'
        re_find_value = r".*name=\"sessionId\" id=\"sessionId\" value=\"(.*)\".*"
        return self.__parse_session_data(find_line, re_find_value)
       
    def __get_game_url(self):
        find_line = 'action="http://prodgame'
        re_find_value = r".*action=\"(.*)\/.*\".*"
        return self.__parse_session_data(find_line, re_find_value)
    
    def __get_world_id(self):
        find_line = 'value="World ' 
        re_find_value = r".*value=\"(.*)\".*"
        return self.__parse_session_data(find_line, re_find_value)
    

    #TODO: replace echo/grep logic with a call to re.search for consistency      
    def __parse_session_data(self, find_line, re_find_value ):
        data = self.session_data
        p1 = Popen(["echo", data], stdout=PIPE)
        p2 = Popen(["grep", find_line], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        line = p2.communicate()[0]
        pattern = re.compile(re_find_value)
        result = pattern.match(line)
        return result.group(1)
    
