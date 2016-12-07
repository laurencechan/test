# coding=utf-8
from tools.py_class import ClassTool
from conn import MongoHelp
from model import ModVerify

__author__ = 'dolacmeo'
__doc__ = '权限系统'


class PermissionMod(ClassTool):
    def __init__(self, user_info=None):
        ClassTool.__init__(self)
        self.__conn = MongoHelp('Permission')
        self.__conn_user = MongoHelp('User')
        self.__conn_settings = MongoHelp('Setting')
        self.__permission_model = self.__conn_settings.find_one({"set_type": "permission_model"})
        from user import User
        if isinstance(user_info, User):
            self.user = user_info
            self.__allow_list = self.__allow()

    def __allow(self):
        if self.user.group == 'super':
            return MongoHelp('Setting').find_one({'set_type': 'system'})['all_fuc'].keys()
        return self.user.user_data['permission']['tag'].keys()

    @ModVerify
    def grant(self, ident, func_name, class_list=None):
        print self.__allow_list
        the_user = self.__conn_user.find_one({'username': ident})
        if func_name not in the_user['permission']['tag'].keys():
            tag = the_user['permission']['tag']
            if class_list is None:
                tag[func_name] = []
            else:
                tag[func_name] = [class_list]
            is_update = self.__conn_user.fix_one({'_id': the_user['_id']},
                                                 {'permission': {'tag': tag, 'group': the_user['permission']['group']}})
            return self._sys_msg(is_update, 'Grant Fail', {'_id': the_user['_id']})
        else:
            permission_keys = the_user['permission']['tag'][func_name]
            tag = the_user['permission']['tag']
            if isinstance(class_list, unicode):
                if class_list in permission_keys:
                    pass
                else:
                    permission_keys.append(class_list)
                    class_list = permission_keys
            elif isinstance(class_list, list):
                for key in permission_keys:
                    if key in class_list:
                        pass
                    else:
                        class_list.append(key)
            if not class_list:
                class_list = []
            tag[func_name] = class_list
            is_update = self.__conn_user.fix_one({'_id': the_user['_id']},
                                                 {'permission': {'tag': tag, 'group': the_user['permission']['group']}})
            return self._sys_msg(is_update, 'Grant Fail', {'_id': the_user['_id']})

    @ModVerify
    def revoke(self, ident, func_name, class_list=None):
        print self.__allow_list
        the_user = self.__conn_user.find_one({'username': ident})
        if func_name in the_user['permission']['tag'].keys():
            permission_keys = the_user['permission']['tag'][func_name]
            if isinstance(class_list, list):
                for key in class_list:
                    if key in permission_keys:
                        permission_keys.remove(key)
                    else:
                        pass
            elif isinstance(class_list, unicode):
                if class_list in permission_keys:
                    permission_keys.remove(class_list)
                else:
                    pass
            else:
                pass
            tag = the_user['permission']['tag']
            if not permission_keys:
                pass
            else:
                tag[func_name] = permission_keys
            if permission_keys:
                is_update = self.__conn_user.fix_one({'_id': the_user['_id']},
                                                     {'permission': {'tag': tag,
                                                                     'group': the_user['permission']['group']}})
                return self._sys_msg(is_update, 'Grant Fail', {'_id': the_user['_id']})
            else:
                tag = the_user['permission']['tag']
                del tag[func_name]
                is_update = self.__conn_user.fix_one({'_id': the_user['_id']},
                                                     {'permission': {'tag': tag,
                                                                     'group': the_user['permission']['group']}})
                return self._sys_msg(is_update, 'Grant Fail', {'_id': the_user['_id']})
        else:
            return self._sys_msg(True, ext_json={'_id': the_user['_id']})
        pass

    @ModVerify
    def setup_model(self, user_model, func_name, class_list=None, is_fix=False):
        if class_list is None:
            class_list = []
        if user_model in self.__permission_model['tag'].keys() and not is_fix:
            return self._sys_msg(False, 'Already have')
        else:
            self.__permission_model['tag'][user_model] = {func_name: sorted(class_list)}
        is_insert = self.__conn_settings.fix_one({"set_type": "permission_model"},
                                                 {'tag': self.__permission_model['tag']})
        return self._sys_msg(is_insert, 'Setup Fail')

    @ModVerify
    def remove_model(self, user_model):
        del self.__permission_model['tag'][user_model]
        is_delete = self.__conn_settings.fix_one({"set_type": "permission_model"},
                                                 {'tag': self.__permission_model['tag']})
        return self._sys_msg(is_delete, 'Delete Fail')

    @ModVerify
    def details(self, _id):
        found = self.__conn_user.find_one({'_id': _id})
        return self._sys_msg(found, 'Not Found')

    @ModVerify
    def get_list(self, ident=None, limit=10, skip=0):
        if ident is None:
            ident = {'reviewed': True}
        found = self.__conn_user.conn.find(ident).limit(limit).skip(skip)
        total = found.count()
        user_data = self.__conn_user.id_format(found)
        return self._sys_msg(user_data, 'Grant Fail', {'page': {'total': total, 'limit': limit, 'skip': skip}})

    pass


if __name__ == '__main__':
    print PermissionMod().fuc
    pass
