# coding=utf-8
import hashlib
import datetime
from tools.py_class import ClassTool
from conn import MongoHelp
from model import ModVerify

__author__ = 'dolacmeo'
__doc__ = '用户系统'

ran_char = '0123456789' \
           'abcdefghijklmnopqrstuvwxyz' \
           'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
           '`~!@#$%^&*()-_=+\|[]{};:,.<>/?'


class User:
    def __init__(self, **kwargs):
        for i in ['ident', 'pwd', 'apikey', 'visitor']:
            if i in kwargs:
                break
        else:
            raise Exception('Login Fail')
        self.__conn_user = MongoHelp('User')
        self.__conn_setting = MongoHelp('Setting').find_one({'set_type': 'system'})
        self.user_data, self.is_login, self.group, self.permission = None, False, None, None
        if kwargs.get('visitor', False):
            self.__visitor_login()
        elif kwargs.get('apikey', False):
            self.__apikey_login(kwargs['apikey'])
        else:
            self.__user_login((kwargs['ident'], kwargs['pwd']))
        pass

    def __user_login(self, user_ident):
        self.__salt = self.__conn_setting['user_salt']
        if user_ident[0] == 'super':
            if self.__conn_setting['super_user']['disable']:
                print 'Super is Disable'
                user_data = None
            else:
                user_data = self.__conn_user.find_one({'_id': self.__conn_setting['super_user']['_id']})
        else:
            if user_ident[0].isdigit() and len(user_ident[0]) == 11:
                ident = 'phone'
            else:
                ident = 'username'
            user_data = self.__conn_user.find_one({ident: user_ident[0]})
        if user_data:
            if user_data['username'] == 'super':
                salt = self.__conn_setting['super_user']['salt']
            else:
                salt = self.__salt
            if user_data['password'] == hashlib.md5(salt + user_ident[1] + salt).hexdigest():
                self.user_data = user_data
                self.is_login = True
                self.group = user_data['permission']['group']
                self.permission = user_data['permission']['tag']
                print user_data['username'] + ' is Login'
            else:
                print user_data['username'] + ' Login Fail'
            if 'reset_code' in user_data.keys():
                self.__conn_user.fix_one({'_id': user_data['_id']}, {'reset_code': 1}, '$unset')
        else:
            print 'User not found'

    def __visitor_login(self):
        if self.__conn_setting['vistor_user']['disable']:
            raise
        visitor = self.__conn_user.find_one({'_id': self.__conn_setting['vistor_user']['_id']})
        self.user_data = visitor
        self.is_login = True
        self.group = visitor['permission']['group']
        self.permission = visitor['permission']['tag']
        print visitor['username'] + ' is Login'
        
    def __apikey_login(self, apikey):
        if not self.__conn_setting.get('api_func', True):
            raise
        api_user = self.__conn_user.find_one({'apikey': apikey})
        if api_user:
            self.user_data = api_user
            self.is_login = True
            self.group = api_user['permission']['group']
            self.permission = api_user['permission']['tag']
            print api_user['username'] + ' is Login'
        else:
            print apikey + ' Login Fail'

    def set_apikey(self):
        if not self.is_login:
            return {'success': False, '_id': '', 'apikey': '', 'error': 'Login Failed'}
        user_apikey = self.user_data.get('apikey', '')
        if user_apikey:
            return {'success': True, '_id': self.user_data['_id'], 'apikey': user_apikey, 'error': ''}
        import random
        while True:
            if not self.__conn_user.find({'apikey': user_apikey}):
                break
            user_apikey = hashlib.md5("".join(random.sample(ran_char, 32))).hexdigest().upper()
        is_set = self.__conn_user.fix_one({'_id': self.user_data['_id']}, {'apikey': user_apikey})
        if is_set:
            return {'success': True, '_id': self.user_data['_id'], 'apikey': user_apikey, 'error': ''}
        else:
            return {'success': False, '_id': self.user_data['_id'], 'apikey': '', 'error': 'Set apikey Failed'}

    def unset_apikey(self):
        if not self.is_login:
            return {'success': False, '_id': '', 'apikey': '', 'error': 'Login Failed'}
        is_set = self.__conn_user.fix_one({'_id': self.user_data['_id']}, {'apikey': 1}, '$unset')
        if is_set:
            return {'success': True, '_id': self.user_data['_id'],  'error': ''}
        else:
            return {'success': False, '_id': self.user_data['_id'], 'error': 'Unset apikey Failed'}

    def info_update(self, info):
        if not self.is_login:
            return {'success': False, '_id': '', 'apikey': '', 'error': 'Login Failed'}
        user_data = self.user_data
        user_id = user_data['_id']
        user_default = MongoHelp('Setting').find_one({'set_type': 'raw_data'})['user_default']
        for n in info.keys():
            if n not in ['username', 'password'] and n in user_default.keys():
                if n != 'permission':
                    if isinstance(info[n], str):
                        user_data[n] = info[n]
                    elif isinstance(info[n], dict):
                        for m in info[n].keys():
                            user_data[n][m] = info[n][m]
        for i in ['_id', 'username', 'password']:
            del user_data[i]
        is_update = self.__conn_user.fix_one({'_id': user_id}, user_data)
        if is_update:
            return {'success': True, '_id': user_id, 'apikey': '', 'error': ''}
        else:
            return {'success': False, '_id': user_id, 'apikey': '', 'error': 'Update Failed'}

    pass


class UserMod(ClassTool):
    def __init__(self, user_info=None):
        ClassTool.__init__(self)
        if isinstance(user_info, User):
            self.user = user_info
            self.__conn = MongoHelp('User')
            self.__conn_setting = MongoHelp('Setting').find_one({'set_type': 'system'})
            self.__salt = self.__conn_setting['user_salt']
            self.__raw_data = MongoHelp('Setting').find_one({'set_type': 'raw_data'})
            self.__permission = self.__raw_data['permission']
            self.__group_range = MongoHelp('Permission').find_one({'group_name': self.user.group})['control']
        else:
            # raise Exception('Plz input User case')
            pass

    @ModVerify
    def create(self, username, password, phone='', group='user', info=None):
        if len(password) < 6:
            return self._sys_msg(False, {'_id': ''}, 'password need more then 6 char')
        if username.isdigit():
            return self._sys_msg(False, {'_id': ''}, 'username fail with only numbers')
        if not self.__group_range:
            return self._sys_msg(False, {'_id': ''}, 'Need create_user Permission')
        is_old_nicename = self.__conn.find_one({'username': username})
        is_old_phone = self.__conn.find_one({'phone': phone})
        if is_old_nicename or (is_old_phone and phone):
            return self._sys_msg(False, {'_id': ''}, 'username already in')
        else:
            user_default = self.__raw_data['user_default']
            new_user = dict(
                username=username,
                password=hashlib.md5(self.__salt + password + self.__salt).hexdigest(),
                phone=phone if phone.isdigit() and (len(phone) == 11) else '',
                permission=dict(group=group if group in self.__group_range else 'user',
                                tag={}),
                create_date=datetime.datetime.now()
            )
            if info:
                new_user.update(info)
            user_default.update(new_user)
            return self._sys_msg(True, ext_json={'_id': self.__conn.insert(user_default)})

    @ModVerify
    def modify(self, ident, info):
        if not info or not isinstance(info, dict):
            raise Exception('Update what? need dict data')
        if not self.__group_range:
            raise Exception('Need update_user Permission')
        if ident.isdigit() and len(ident) == 11:
            key = 'phone'
        else:
            key = 'username'
        user_data = self.__conn.find_one({key: ident})
        if not user_data:
            return self._sys_msg(False, 'ident error, check out!', {'_id': ''})
        user_id = user_data['_id']
        user_default = self.__raw_data['user_default']
        for n in info.keys():
            if n not in ['username', 'password'] and n in user_default.keys():
                if n == 'permission':
                    if info[n].get('group') not in self.__group_range:
                        return self._sys_msg(False, 'Permission Limit', {'_id': ''})
                    else:
                        if 'group' in info[n].keys():
                            user_data[n]['group'] = info[n]['group']
                        if 'tag' in info[n].keys():
                            system_mod = MongoHelp('Setting').find_one({'set_type': 'system'})['all_fuc'].keys()
                            for m in info[n].keys():
                                if m in system_mod:
                                    if m in user_data[n]['tag'].keys():
                                        user_data[n]['tag'][m].extend(info[n][m])
                                    else:
                                        user_data[n]['tag'][m] = info[n][m]
                else:
                    if isinstance(info[n], str):
                        user_data[n] = info[n]
                    elif isinstance(info[n], dict):
                        for m in info[n].keys():
                            user_data[n][m] = info[n][m]
        for i in ['_id', 'username', 'password']:
            del user_data[i]
        is_update = self.__conn.fix_one({'_id': user_id}, user_data)
        return self._sys_msg(is_update, 'Update Failed', {'_id': is_update})

    @ModVerify
    def details(self, _id):
        found = self.__conn.find_one({'_id': _id})
        return self._sys_msg(found, 'Not Found')

    @ModVerify
    def get_list(self, ident=None, limit=10, skip=0):
        if ident is None:
            ident = {}
        found = self.__conn.conn.find(ident).limit(limit).skip(skip)
        total = found.count()
        found = self.__conn.id_format(found)
        return self._sys_msg(found, 'Grant Fail', {'page': {'total': total, 'limit': limit, 'skip': skip}})

    @staticmethod
    def reset_pwd(is_request=True, **kwargs):
        db_conn = MongoHelp('User')
        if is_request:
            if 'username' not in kwargs.keys():
                raise Exception('Need username to request reset password!')
            try:
                import random
                reset_code = '%06d' % random.randint(0, 999999)
                db_conn.fix_one({'username': kwargs['username']},
                                {'reset_code': reset_code})
                return {'success': True, 'reset_code': reset_code,
                        'error': '', 'fuc_name': 'UserMod#reset_pwd'}
            except Exception, e:
                return {'success': False, 'reset_code': '',
                        'error': 'reset_pwd: %s' % e, 'fuc_name': 'UserMod#reset_pwd'}
        else:
            for n in ['username', 'code', 'newpwd']:
                if n not in kwargs.keys():
                    raise Exception('Need %s to reset password!' % n)
            user_data = db_conn.find_one({'username': kwargs['username']})
            if kwargs['code'] == user_data.get('reset_code'):
                salt = MongoHelp('Setting').find_one({'set_type': 'system'})['user_salt']
                user_data['password'] = hashlib.md5(salt + kwargs['newpwd'] + salt).hexdigest()
                user_id = user_data['_id']
                for i in ['_id', 'reset_code']:
                    del user_data[i]
                print user_data
                is_reset = db_conn.fix_one({'_id': user_id}, user_data)
                if is_reset:
                    db_conn.fix_one({'_id': user_id}, {'reset_code': 1}, '$unset')
                    return {'success': True, '_id': user_id,
                            'error': '', 'fuc_name': 'UserMod#reset_pwd'}
                else:
                    return {'success': False, '_id': user_id,
                            'error': 'reset_pwd UNKNOW ERROR', 'fuc_name': 'UserMod#reset_pwd'}
            else:
                return {'success': False, '_id': '',
                        'error': 'reset_code ERROR or need request', 'fuc_name': 'UserMod#reset_pwd'}

    pass


if __name__ == '__main__':
    # print UserMod('jack2', 'roessdf').create_user('jack3', 'roessdf', '15645678759')
    # print [n for n in dir(UserMod) if n[0] != '_']
    # print UserMod().fuc
    # print UserMod('jack', 'roes').fuc
    # print UserMod(User(ident='jack', pwd='roes')).create_user('test', 'okok', '15645678759')
    # print User(ident='super', pwd='superadmin').user_data
    # admin = User(ident='super', pwd='superadmin')
    # user = User(ident='jack', pwd='jackroes')
    # print UserMod(admin).create('jack', 'jackroes')/
    # print UserMod(user).create('qwertd', 'qwertyuiop')
    # print UserMod(admin).update('qwer', {'infos': {'age': 18}})
    # print User(ident='qwer', pwd='qwertyuiop').user_data
    # print UserMod.get_list()
    # print UserMod.reset_pwd(is_request=False, username='qwer', code='269420', newpwd='qwop1234')
    # print UserMod().fuc
    pass
