# coding=utf-8
from tools.py_class import ClassTool
from conn import MongoHelp
from model import ModVerify

__author__ = 'dolacmeo'
__doc__ = '权限系统'


class CommentMod(ClassTool):
    def __init__(self, user_info=None):
        ClassTool.__init__(self)
        self.__conn = MongoHelp('Comment')
        from user import User
        if isinstance(user_info, User):
            self.user = user_info

    @ModVerify
    def add(self, main_id, comment, level_reply=None, reviewed=False):
        comment_num = self.__conn.conn.find({'main_id': main_id}).count()
        comment_post = dict(
            main_id=main_id,
            level_num=comment_num+1,
            level_reply=level_reply,
            content=comment,
            username=self.user.user_data['username'],
            user_id=self.user.user_data['_id'],
            status='normal',
            reviewed=reviewed
        )
        is_add = self.__conn.insert(comment_post)
        return self._sys_msg(is_add, 'Grant Fail', {'_id': is_add})

    @ModVerify
    def modify(self, comment_id, comment):
        is_fix = self.__conn.fix_one({'_id': comment_id}, {'content': comment})
        return self._sys_msg(is_fix, 'Grant Fail', {'_id': comment_id})

    @ModVerify
    def remove(self, comment_id):
        is_del = self.__conn.remove({'_id': comment_id})
        return self._sys_msg(is_del, 'Grant Fail', {'_id': comment_id})

    @ModVerify
    def review(self, comment_id, is_pass=True):
        is_review = self.__conn.fix_one({'_id': comment_id}, {'reviewed': is_pass})
        return self._sys_msg(is_review, 'Grant Fail', {'_id': comment_id})

    @ModVerify
    def details(self, _id):
        found = self.__conn.find_one({'_id': _id})
        return self._sys_msg(found, 'Not Found')

    @ModVerify
    def get_list(self, ident=None, limit=10, skip=0):
        if ident is None:
            ident = {'reviewed': True}
        found = self.__conn.conn.find(ident).limit(limit).skip(skip)
        total = found.count()
        comment_data = self.__conn.id_format(found)
        return self._sys_msg(comment_data, 'Not Found', {'page': {'total': total, 'limit': limit, 'skip': skip}})


if __name__ == '__main__':
    print CommentMod().fuc
    pass
