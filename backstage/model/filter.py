# coding=utf-8
from core.conn import MongoHelp

__author__ = 'dolacmeo'
__doc__ = ''


class Filter:
    def __init__(self):
        pass
        self.user_conn = MongoHelp('User')

    def username(self, _id):
        return MongoHelp('User').find_one({'_id': _id})['username']

    def content_title(self, _id):
        return MongoHelp('Content').find_one({'_id': _id})['title']

if __name__ == '__main__':
    pass
