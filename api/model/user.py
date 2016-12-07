# coding=utf-8
from core import CMS, User

__author__ = 'dolacmeo'
__doc__ = ''


class UserApi:
    def __init__(self, User_info=None):
        if isinstance(User_info, User):
            self.user = User_info

    def get_apikey(self):
        if not self.user.is_login:
            return {'error': 'Login Error'}
        return self.user.set_apikey()

    def unset_apikey(self):
        if not self.user.is_login:
            return {'error': 'Login Error'}
        return self.user.unset_apikey()

if __name__ == '__main__':
    pass
