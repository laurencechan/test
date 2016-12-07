# coding=utf-8
import datetime
import hashlib
import setting
from core.conn import MongoHelp, mongo_conn
from core.conn import DatabaseInfo as dbInfo

__author__ = 'dolacmeo'
__doc__ = ''

ran_char = '0123456789' \
           'abcdefghijklmnopqrstuvwxyz' \
           'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
           '`~!@#$%^&*()-_=+\|[]{};:,.<>/?'

db_setting = setting.Mongodb_setup.collections


class SystemInit:
    def __init__(self):
        pass

    def db_init(self):
        import ConfigParser
        cf = ConfigParser.ConfigParser()
        cf.add_section('db')
        cf.set('db', 'user_name', setting.Mongodb_setup.user_name)
        cf.set('db', 'pass_word', setting.Mongodb_setup.pass_word)
        cf.set('db', 'address', setting.Mongodb_setup.address)
        cf.set('db', 'db_name', setting.Mongodb_setup.db_name)
        cf.write(open("core/db.conf", "w"))

        if dbInfo().initializing(db_setting):
            print 'OK'
            if 'Setting' not in mongo_conn().collection_names():
                mongo_conn().create_collection('Setting')
            raw_data = MongoHelp('Setting').insert({
                'set_type': 'raw_data',
                'mongodb': setting.Mongodb_setup.collections,
                'permission': setting.Permission.ControlTree,
                'column': setting.Column.ColumnTree,
                'user_default': setting.UserSetting.default,
                'create_time': datetime.datetime.now()
            })
            self.permission_init()
            import random
            super_salt = ''.join(random.sample(ran_char, 16))
            super_user = MongoHelp('User').insert({
                'username': 'super',
                'password': hashlib.md5(super_salt + setting.Permission.super_pass + super_salt).hexdigest(),
                "permission": {"group": "super", "tag": {}}
            })
            user_salt = "".join(random.sample(ran_char, 16))
            visitor_user = MongoHelp('User').insert({
                'username': 'visitor',
                'password': hashlib.md5(user_salt + 'Visitor' + user_salt).hexdigest(),
                "permission": {"group": "user", "tag": {}}
            })
            MongoHelp('Setting').insert({
                'set_type': 'system',
                'raw_data': raw_data,
                "super_user": {
                    "_id": super_user,
                    "salt": super_salt,
                    "disable": False
                },
                "vistor_user": {
                    "_id": visitor_user,
                    "disable": False
                },
                "user_salt": user_salt,
                "all_fuc": setting.ProjectMod.regmod,
                "fuc_name": setting.ProjectMod.modlist,
                "all_column": [n for n in setting.Column.ColumnTree.keys()],
                "content_type": [n for n in setting.ProjectMod.support_content],
                "building_date": datetime.datetime.now(),
                "creater": {
                    "author": "dolacmeo",
                    "compeny": "Heilongjiang New-media Group"
                },
                "api_func": True,
            })
            MongoHelp('Setting').insert({
                'set_type': 'content',
                'content_default': setting.ContentType.__dict__
            })
            self.create_fuc_page()

    @staticmethod
    def create_fuc_page():
        import platform
        import os
        for model in setting.ProjectMod.regmod.keys():
            if platform.system() == 'Windows':
                with open(os.getcwd() + r'\templates\backstage\content\%s.html' % model.split('#')[0], 'w') as f:
                    if not f:
                        f.write('<h1>%s</h1>' % model.split('#')[0])
                    f.close()
            else:
                with open(os.getcwd() + r'/templates/backstage/content/%s.html' % model.split('#')[0], 'w') as f:
                    if not f:
                        f.write('<h1>%s</h1>' % model.split('#')[0])
                    f.close()

    @staticmethod
    def permission_init():
        db_conn = MongoHelp('Permission')
        db_tree, status = db_conn.find({}), {}
        rebuding = setting.Permission.ControlTree
        for role in ['super', 'admin']:
            if role not in setting.Permission.ControlTree.keys():
                raise Exception('Need Permission %s' % role)
        for n in setting.Permission.ControlTree.keys():
            status[n] = False
        for n in db_tree:
            if n['group_name'] in status.keys():
                status[n['group_name']] = True
        if False in status.itervalues():
            for m in status.keys():
                if not status[m]:
                    db_conn.insert(rebuding[m])

    @staticmethod
    def column_init():
        init_list = []
        basecolumn = setting.Column.ColumnTree
        for n in basecolumn.keys():
            init_list.append(dict(
                class_id=n,
                lv_class=n.count('-'),
                father='-'.join(n.split('-')[:-1]),
                title=basecolumn[n]['title'],
                subject=basecolumn[n]['subject'],
                type=basecolumn[n]['type'],
                address='/'.join(
                    ['-'.join([x for x in n.split('-')][:m + 1]) for m in range(len([x for x in n.split('-')]))]),
                include=[]
            ))
        for n in range(len(init_list)):
            if init_list[n]['father']:
                for m in range(len(init_list)):
                    if init_list[m]['class_id'] == init_list[n]['father']:
                        init_list[m]['include'] += [init_list[n]['class_id']]
                        break
                init_list[m]['include'] = sorted(init_list[m]['include'])
        return dbInfo().init_data('Column', init_list)

    def init_process(self):
        try:
            self.db_init()
            self.column_init()
        except Exception, e:
            print e
        else:
            print 'initializing process complete'

    @staticmethod
    def rebuild():
        names = dbInfo().conn.collection_names()
        for name in names:
            dbInfo().conn.drop_collection(name)


if __name__ == '__main__':
    SystemInit().init_process()
    # SystemInit().create_fuc_page()
    # SystemInit().rebuild()
    pass
