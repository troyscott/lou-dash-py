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
        #print 'Response login: %s' % response
        headers = {'Cookie': response['set-cookie']}
        response, content = client.request(_URL_HIDDEN_SESSION_ID, 'GET',
                headers=headers)
        pattern = re.compile(r'.*id="sessionId" value="(.*)".*')
        self.session_id = pattern.search(content).groups()[0]
        pattern = re.compile(r'.*action="(http://prodgame.*/.*/).*".*')
        self.game_url = pattern.search(content).groups()[0]
        pattern = re.compile(r'.*value="(World.*)".*')
        self.world_id = pattern.search(content).groups()[0]

