# -*- coding: utf-8 -*-

from req_handler import *
from helpers import Auth, logger
import pkg_resources
import urllib.parse
import json


class OAuthReqHandler(ReqHandler):

    def oauth(self, s):
        client_id = s.query_components.get("client_id", "")
        redirect_uri = s.query_components.get("redirect_uri", "")
        state = s.query_components.get("state", "")
        response_type = s.query_components.get("response_type", "")
        authCode = s.query_components.get("code", "")

        if 'code' != response_type:
            s.send_message(500, 'response_type %s must equal "code"' % response_type)
            return

        if Auth["clients"].get(client_id, "") == "":
            s.send_message(500, 'client_id %s invalid' % client_id)
            return

        # if there is an authcode use it
        if authCode != "":
            s.redirect('%s?code=%s&state=%s' % (redirect_uri, authCode, state))
            return

        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            print('No user data')
            s.redirect('login?client_id=%s&redirect_uri=%s&redirect=%s&state=%s' %
                       (client_id, urllib.parse.quote(redirect_uri, safe=''), s.only_path, state))
            return

        authCode = self.generateAuthCode(user['uid'], client_id)

        if authCode is not None:
            s.redirect('%s?code=%s&state=%s' % (redirect_uri, authCode, state))
            return

        s.send_message(400, "Something went wrong")

    def login(self, s):
        template = pkg_resources.resource_string(__name__, 'templates/login.html')

        headers = {"Cache-Control": "no-cache"}
        s.send_message(200, template, headers, True)

    def login_post(self, s):
        user = self.getUser(s.form.get("username", None), s.form.get("password", None))

        if user is None:
            if s.headers['X-Forwarded-For'] is None:
                logger.error("Failed login from %s", s.address_string())
            else:
                logger.error("Failed login from %s", s.headers['X-Forwarded-For'])
            s.redirect('login?client_id=%s&redirect_uri=%s&redirect=%s&state=%s' %
                       (s.form.get("client_id", None), s.form.get("redirect_uri", None), s.form.get("redirect", None),
                        s.form.get("state", None)), 301)
            return

        self.setSessionUser(user)
        authCode = self.generateAuthCode(user['uid'], s.form.get("client_id", None))

        if authCode is not None:
            s.redirect('%s?code=%s&state=%s' % (
                urllib.parse.unquote(urllib.parse.unquote(s.form.get("redirect_uri", None))), authCode,
                s.form.get("state", None)), 301)
            return

        s.send_message(500, "Internal server error")

    # /**
    # * client_id=GOOGLE_CLIENT_ID
    # * &client_secret=GOOGLE_CLIENT_SECRET
    # * &response_type=token
    # * &grant_type=authorization_code
    # * &code=AUTHORIZATION_CODE
    # *
    # * OR
    # *
    # *
    # * client_id=GOOGLE_CLIENT_ID
    # * &client_secret=GOOGLE_CLIENT_SECRET
    # * &response_type=token
    # * &grant_type=refresh_token
    # * &refresh_token=REFRESH_TOKEN
    # */
    def token_post(self, s):
        client_id = s.query_components.get("client_id", s.form.get("client_id", None))
        client_secret = s.query_components.get("client_secret", s.form.get("client_secret", None))
        grant_type = s.query_components.get("grant_type", s.form.get("grant_type", None))

        if client_id is None or client_secret is None:
            s.send_message(400, "missing required parameter")
            return

        client = self.getClient(client_id, client_secret)
        if client is None:
            s.send_message(400, "incorrect client data")
            return

        if 'authorization_code' == grant_type:
            self.handleAuthCode(s)
        elif 'refresh_token' == grant_type:
            self.handleRefreshToken(s)
        else:
            s.send_message(400, 'grant_type ' + grant_type + ' is not supported')

    # /**
    # * @return {{}}
    # * {
    # *   token_type: "bearer",
    # *   access_token: "ACCESS_TOKEN",
    # *   refresh_token: "REFRESH_TOKEN"
    # * }
    # */
    def handleAuthCode(self, s):
        client_id = s.query_components.get("client_id", s.form.get("client_id", None))
        client_secret = s.query_components.get("client_secret", s.form.get("client_secret", None))
        code = s.query_components.get("code", s.form.get("code", None))

        if code is None:
            s.send_message(400, "missing required parameter")
            return

        client = self.getClient(client_id, client_secret)
        if client is None:
            s.send_message(400, "incorrect client data")
            return

        authCode = self.authCode(code)
        if authCode is None:
            s.send_message(400, "invalid or expired code")
            return

        if authCode['clientId'] != client_id:
            s.send_message(400, "invalid code - wrong client")
            return

        token = self.getAccessToken(code)
        if token is None:
            s.send_message(400, "unable to generate a token")
            return

        s.send_json(200, token)

    # /**
    # * @return {{}}
    # * {
    # *   token_type: "bearer",
    # *   access_token: "ACCESS_TOKEN",
    # * }
    # */
    def handleRefreshToken(self, s):
        client_id = s.query_components.get("client_id", s.form.get("client_id", None))
        client_secret = s.query_components.get("client_secret", s.form.get("client_secret", None))
        refresh_token = s.query_components.get("refresh_token", s.form.get("refresh_token", None))

        client = self.getClient(client_id, client_secret)
        if client is None:
            s.send_message(500, "incorrect client data")
            return

        if refresh_token is None:
            s.send_message(500, "missing required parameter")
            return

        returnToken = {'token_type': 'bearer', 'access_token': refresh_token}
        s.send_json(200, json.dumps(returnToken))

    # Helper function
    def getAccessToken(self, code):
        authCode = self.authCode(code)
        if authCode is None:
            return None

        user = Auth['users'].get(authCode['uid'], None)
        if user is None:
            return None

        accessToken = Auth['tokens'].get(user['tokens'][0], None)
        if accessToken is None:
            return None

        returnToken = {'token_type': 'bearer', 'access_token': accessToken['accessToken'],
                       'refresh_token': accessToken['refreshToken']}

        return json.dumps(returnToken)


oauthGetMappings = {"/oauth": OAuthReqHandler.oauth,
                    "/login": OAuthReqHandler.login}

oauthPostMappings = {"/login": OAuthReqHandler.login_post,
                     "/token": OAuthReqHandler.token_post}
