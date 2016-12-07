# coding=utf-8
from core import CMS

__author__ = 'dolacmeo'
__doc__ = ''


class CommentApi:
    def __init__(self, User_info=None):
        from core import User
        if isinstance(User_info, User):
            self.user = User_info

    def add_comment(self, content_id, comment, **setup):
        return CMS(self.user).CommentMod().add_comment(content_id, comment, **setup)

    def get_comment(self, content_id):
        return CMS(self.user).CommentMod().get_comment(content_id, True)

if __name__ == '__main__':
    pass
