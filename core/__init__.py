# coding=utf-8
__author__ = 'dolacmeo'
__doc__ = '整合CMS功能模块'


class CMS:

    def __init__(self, user_info):
        from user import User
        if isinstance(user_info, User):
            self.user = user_info
            self.all_func = self.__get_funcs()
        else:
            raise Exception('Need UserMod')
        pass

    def __get_funcs(self):
        all_func = []
        for mod in [n for n in dir(self.__class__) if 'Mod' in n]:
            all_func.extend(getattr(self, mod)().fuc)
        sys_reg = self.Setting_setup().find_one({'set_type': 'system'})['all_fuc']
        if len(all_func) > len(sys_reg):
            print 'There is some new funcs'
            new_fuc = {}
            for name in all_func:
                if name not in sys_reg:
                    new_fuc[name] = raw_input('Need New Modfunc Name [%s]:' % name)
            new_fuc.update(sys_reg)
            self.Setting_setup().fix_one({'set_type': 'system'}, {'all_fuc': new_fuc})
        elif len(all_func) < len(sys_reg):
            print '=' * 40
            print 'Your System version older then database \n or \nDatabase system setting error'
            print '=' * 40
        return all_func

    @staticmethod
    def setting_info(set_type):
        from conn import MongoHelp
        return MongoHelp('Setting').find_one({'set_type': set_type})

    def Setting_setup(self):
        from conn import MongoHelp
        return MongoHelp('Setting')

    @staticmethod
    def column_info(json_data=None, muilt=False):
        if json_data is None:
            json_data = {}
        from conn import MongoHelp
        if muilt:
            return MongoHelp('Column').find(json_data)
        else:
            return MongoHelp('Column').find_one(json_data)

    def UserMod(self):
        from user import UserMod
        return UserMod(self.user)

    def PermissionMod(self):
        from permission import PermissionMod
        return PermissionMod(self.user)

    def ContentMod(self):
        from content import ContentMod
        return ContentMod(self.user)

    def CommentMod(self):
        from comment import CommentMod
        return CommentMod(self.user)

    def PushMod(self):
        from push import PushMod
        return PushMod(self.user)

    @staticmethod
    def FileService():
        from tools.file_service import FileService
        return FileService()

    pass

if __name__ == '__main__':
    cms = CMS()
    getattr(getattr(cms, mod_name)(), fuc_name)(**kwargs)
    pass
