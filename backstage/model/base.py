# coding=utf-8

__author__ = 'dolacmeo'
__doc__ = ''

ran_char = '0123456789' \
           'abcdefghijklmnopqrstuvwxyz' \
           'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
           '`~!@#$%^&*()-_=+\|[]{};:,.<>/?'


class BaseFunc:
    def __init__(self, user_info=None):
        from core.user import User
        if isinstance(user_info, User):
            self.user = user_info
            if not self.user.is_login:
                raise Exception('Login first')

    def setup_regester_fuc(self):
        from core import CMS
        import random
        username = "".join(random.sample(ran_char, 16))
        password = "".join(random.sample(ran_char, 16))
        core = CMS(self.user)
        is_create = core.UserMod().create(username=username, password=password, group='admin')
        if not is_create['success']:
            raise Exception('Unknow error cant create regester admin')
        is_setup = core.Setting_setup().fix_one({'set_type': 'system'},
                                                {'regester_admin': dict(username=username, password=password)})
        if not is_setup:
            raise Exception('Unknow error cant setup setting regester admin')
        return {'success': True}

    @staticmethod
    def user_regester(username, password, phone=''):
        from core import CMS
        setting = CMS.setting_info('system')
        if 'regester_admin' in setting.keys():
            setting = setting['regester_admin']
            from core.user import User
            login = CMS(User(ident=setting['username'], pwd=setting['password']))
            is_regester = login.UserMod().create(username, password, phone)
            if not is_regester['success']:
                raise Exception('Unknow error cant create user')
            return {'success': True}
        else:
            raise Exception('setup regester fuc first!')

    @staticmethod
    def get_column_html(base_dir):
        import os
        import platform
        column_dir = base_dir + r'\templates\backstage\content\column'. \
            replace(r'\\',  r'/' if platform.system() != 'Windows'else r'\\')
        return os.listdir(column_dir)


if __name__ == '__main__':
    pass
