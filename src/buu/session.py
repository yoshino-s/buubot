import requests
from json import load

class BuuUnauthorized(Exception):
    pass

class Session(requests.sessions.Session):
    def __init__(self, url):
        requests.Session.__init__(self)
        self.baseurl = url
        token = None
        try:
            with open('session') as f:
                token = f.read()
        except:
            pass
        if not self.test(token):
            token = input('Input new token:')
            if not self.test(token):
                raise Exception('Session init fail.Can not get a valid session_id')
    
    def test(self, token=None):
        raw_token = self.cookies.get('session')
        if token:
            self.cookies.set('session', token, domain='buuoj.cn')
        resp = self.get(self.baseurl + '/challenges', allow_redirects=False)
        if token and not resp.is_redirect:
            self.save_token(token)
        else:
            self.cookies.set('session', raw_token, domain='buuoj.cn')
        return not resp.is_redirect
    
    def request(self, *args, **kargs):
        resp = super().request(*args, **kargs)
        if resp.url.startswith(self.baseurl + '/login'):
            raise BuuUnauthorized()
        return resp
    
    @staticmethod
    def save_token(token):
        with open('session', 'w') as f:
            f.write(token)
         
s = Session('https://buuoj.cn')