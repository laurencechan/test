# coding=utf-8

from gen_apikey import gen_key

__author__ = 'dolacmeo'
__doc__ = ''


class APIModel:
    def __init__(self, **kwargs):
        from core.user import User
        self.user = User(**kwargs)
        pass

    def user(self):
        from .user import UserApi
        return UserApi(self.user)

    def column(self):
        from .column import ColumnApi
        return ColumnApi(self.user)

    def comment(self):
        from .comment import CommentApi
        return CommentApi(self.user)

if __name__ == '__main__':
    pass
