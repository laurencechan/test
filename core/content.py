# coding=utf-8
import datetime
from tools.py_class import ClassTool
from conn import MongoHelp
from model import ModVerify

__author__ = 'dolacmeo'
__doc__ = '内容系统'


class ContentMod(ClassTool):
    def __init__(self, user_info=None):
        ClassTool.__init__(self)
        self.__conn = MongoHelp('Content')
        from user import User
        if isinstance(user_info, User):
            self.user = user_info

    def __set_classid(self, class_id):
        self.req_permisssion = class_id
        self.__class_id = class_id
        self.__class_info = MongoHelp('Column').find_one({'class_id': class_id})
        if self.__class_info['type'] not in MongoHelp('Setting').find_one(
                {'set_type': 'content'})['content_default'].keys():
            raise Exception('Content set Error: %s' % self.__class_info['type'])
        self.__content_default = MongoHelp('Setting').find_one(
            {'set_type': 'content'})['content_default'][self.__class_info['type']]['data']

    @staticmethod
    def _set_type(default, input_data):
        if isinstance(default, unicode):
            if default.split(',')[0] == 'str':
                default = input_data
            elif default.split(',')[0] == 'int':
                default = int(input_data)
            elif default.split(',')[0] == 'datetime':
                default = datetime.datetime.strptime(input_data, "%Y-%m-%d %H:%M:%S").date()
                # default = input_data
            else:
                default = default.split(',')[2]
            return default
        elif isinstance(default, dict):
            new = {}
            for n in default.keys():
                new[n] = ContentMod._set_type(default[n], input_data[n])
            return new
        elif isinstance(default, list):
            new = []
            for n in input_data:
                new.append(ContentMod._set_type(default[0], n))
            return new

    def _data_format(self, json_data):
        format_data = dict(content_type=self.__class_info['type'],
                           status='normal',
                           reviewed=False,
                           class_id=self.__class_id,
                           statistics={})
        format_data['data'] = ContentMod._set_type(self.__content_default, json_data)
        return format_data

    @ModVerify
    def insert(self, class_id, content_json):
        self.__set_classid(class_id)
        content_json['author_name'] = self.user.user_data['username']
        content_json['author_id'] = self.user.user_data['_id']
        content_data = self._data_format(content_json)
        content_data['addtime'] = datetime.datetime.now()
        content_data['title'] = content_data['data'].get('title', '')
        content_data['author_id'] = self.user.user_data['_id']
        is_insert = self.__conn.insert(content_data)
        return self._sys_msg(is_insert, 'Grant Fail', {'_id': is_insert})

    @ModVerify
    def modify(self, content_id, content_json):
        content_json['author_name'] = self.user.user_data['username']
        content_json['author_id'] = self.user.user_data['_id']
        content_data = self._data_format(content_json)
        is_update = self.__conn.fix_one({'_id': content_id}, content_data)
        return self._sys_msg(is_update, 'Grant Fail', {'_id': content_id})

    @ModVerify
    def remove(self, content_id):
        is_remove = self.__conn.remove({'_id': content_id})
        return self._sys_msg(is_remove, 'Grant Fail', {'_id': content_id})

    @ModVerify
    def review(self, content_id, is_pass=True):
        is_reviewed = self.__conn.fix_one({'_id': content_id}, {'reviewed': is_pass})
        return self._sys_msg(is_reviewed, 'Grant Fail', {'_id': content_id})

    @ModVerify
    def details(self, _id):
        found = self.__conn.find_one({'_id': _id})
        return self._sys_msg(found, 'Not Found')

    @ModVerify
    def get_list(self, ident=None, limit=10, skip=0):
        ident_json = {}
        if isinstance(ident, dict):
            ident_json.update(ident)
        found = self.__conn.conn.find(ident_json, {'data': 0}).limit(limit).skip(skip)
        total = found.count()
        found = self.__conn.id_format(found)
        reviewed = self.__conn.conn.find({'reviewed': True}).count()
        return self._sys_msg(found, 'Grant Fail', {'page': {'total': total, 'limit': limit,
                                                            'skip': skip, 'reviewed': reviewed}})

    pass


if __name__ == '__main__':
    print ContentMod().fuc
    data = {"content": "这是一段普通的测试内容啊啊啊啊啊啊啊啊",
            "title": "测试文章abcd",
            "author_name": "作者名字",
            "author_id": "57ce5af90b0555043c60e7d9",
            "from": "文章来源火星",
            "thumbnail": "http://ajcreative.net/wp-content/uploads/2014/12/blog-head.jpg",
            "images": [{
                "img_src": "https://www.baidu.com/img/baidu_jgylogo3.gif",
                "description": "这是百度logo",
                "url_to": "https://www.baidu.com/"
            },
                {
                    "img_src": "https://www.baidu.com/img/baidu_jgylogo3.gif",
                    "description": "这是百度logo",
                    "url_to": "https://www.baidu.com/"
                }
            ]}
    # from user import User
    # admin = User(ident='super', pwd='superadmin')
    # user = User(ident='jack', pwd='jackroes')
    # test = ContentMod(user, '1-1').insert(data)
    # print test
    pass
