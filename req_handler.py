# -*- coding: utf-8 -*-

import time
import uuid
from http.cookies import SimpleCookie as Cookie

from const import (SESSION_TIMEOUT, AUTH_CODE_TIMEOUT)
from helpers import Auth


class ReqHandler:
    sessioncookies = {}
    userdata = {}
    sessionid = ''

    authcodes = {}

    # hardcoded data for test only!!!
    # authcodes = {'1':{ 'type': 'AUTH_CODE', 'uid': '1234', 'clientId': 'AxjqWpsYj4', 'expiresAt': time.time() + 10000000}} #should be empty

    def _session_cookie(self, s, forcenew=False):
        new_cookie = False

        cookiestring = "\n".join(s.headers.get_all('Cookie', failobj=[]))
        c = Cookie()
        c.load(cookiestring)

        # clear old session_id's
        self.sessioncookies = {k: v for k, v in self.sessioncookies.items() if time.time() - v < SESSION_TIMEOUT}
        common = self.sessioncookies.keys() & self.userdata.keys()
        self.userdata = {k: v for k, v in self.userdata.items() if k in common}

        try:
            if forcenew or time.time() - self.sessioncookies[c['aog_session_id'].value] > SESSION_TIMEOUT:
                raise ValueError('new cookie needed')
        except (ValueError, Exception):
            new_cookie = True
            c['aog_session_id'] = uuid.uuid4().hex
            self.userdata[c['aog_session_id'].value] = {}

        for m in c:
            if m == 'aog_session_id':
                self.sessioncookies[c[m].value] = time.time()
                c[m]["httponly"] = True
                c[m]["max-age"] = SESSION_TIMEOUT
                c[m]["expires"] = s.date_time_string(time.time() + SESSION_TIMEOUT)
                self.sessionid = c[m].value
                return new_cookie, c[m]

        return new_cookie, None

    def getSessionUser(self):
        return self.userdata.get(self.sessionid, None)

    def setSessionUser(self, user):
        self.userdata[self.sessionid] = user

    def generateAuthCode(self, uid, client_id):
        authCode = uuid.uuid4().hex
        c = {'type': 'AUTH_CODE', 'uid': uid, 'clientId': client_id, 'expiresAt': time.time() + AUTH_CODE_TIMEOUT}
        self.authcodes[authCode] = c
        return authCode

    def authCode(self, code):
        self.authcodes = {k: v for k, v in self.authcodes.items() if v['expiresAt'] > time.time()}

        ac = self.authcodes.get(code, "")
        if ac != "":
            if ac['expiresAt'] > time.time():
                return ac
        return None

    @staticmethod
    def getUser(username, passwd):
        userId = Auth["usernames"].get(username, None)
        if userId is not None:
            user = Auth["users"].get(userId, None)
            if user is not None:
                if user['password'] == passwd:
                    return user

        return None

    @staticmethod
    def getClient(clientid, clientsecret):
        client = Auth["clients"].get(clientid, None)
        if client is None or client['clientSecret'] != clientsecret:
            return None

        return client

    def getUserAgent(self):
        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            return None
        accessToken = Auth['tokens'].get(user['tokens'][0], None)
        if accessToken is None:
            return None

        return accessToken['userAgentId']
