# coding=utf-8
from conn import MongoHelp

__author__ = 'dolacmeo'
__doc__ = ''


class FileService:

    def __init__(self):
        self.conn = MongoHelp('Images')

    def save(self, f, **setting):
        return self.conn.save_file(f, **setting)

    def update(self, sha1, info_dict):
        return self.conn.fix_one({'sha1': sha1}, {'info': info_dict})

    def load(self, sha1):
        return self.conn.load_file(sha1)

    def file_list(self, ident, **setting):
        return self.conn.list_file(ident, **setting)

    pass


if __name__ == '__main__':
    pass
