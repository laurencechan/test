# coding=utf-8
from core import CMS

__author__ = 'dolacmeo'
__doc__ = ''


class CMSFrame:
    def __init__(self, user_info=None):
        from core.user import User
        if isinstance(user_info, User):
            self.user = user_info
            if self.user.is_login:
                self.allow_fuc = self.__get_permission()
                self.allow_column = self.__get_column()
            else:
                raise Exception('Login first')

    def __get_permission(self):
        if self.user.group == 'super':
            permission = CMS.setting_info('system')['all_fuc'].keys()
        else:
            permission = self.user.permission.keys()
        # print permission
        data = {}
        for n in list(set([n.split('#')[0] for n in permission])):
            data[n] = {}
            for m in [x.split('#')[1] for x in permission if x.split('#')[0] == n]:
                if self.user.group == 'super':
                    if n in ['ContentMod']:
                        data[n][m] = CMS.setting_info('system')['all_column']
                    else:
                        data[n][m] = []
                else:
                    data[n][m] = self.user.permission[n+'#'+m]
        return data

    def __get_column(self):
        if self.user.group == 'super':
            column = CMS.setting_info('system')['all_column']
        else:
            column = []
            for n in ['ContentMod#insert', 'ContentMod#modify', 'ContentMod#remove', 'ContentMod#search']:
                if n in self.user.permission.keys():
                    column.extend(self.user.permission[n])
            column = list(set(column))

        from collections import defaultdict
        tree = lambda: defaultdict(tree)
        data = tree()

        def add(t, keys, v=None):
            if v is None:
                v = []
            if len(keys) > 1:
                for n in range(len(keys)):
                    if n == len(keys) - 1:
                        t[keys[n]] = v
                    else:
                        t = t[keys[n]]
        for n in column:
            info = CMS.column_info({'class_id': n})
            addr = info['address'].split('/')
            if info['type'] != 'column':
                if self.user.group == 'super':
                    permission = ['ContentMod#insert', 'ContentMod#modify',
                                  'ContentMod#remove', 'ContentMod#search', 'ContentMod#review']
                else:
                    permission = []
                    for m in ['ContentMod#insert', 'ContentMod#modify',
                              'ContentMod#remove', 'ContentMod#search', 'ContentMod#review']:
                        if m in self.user.permission.keys():
                            permission.append(m)
                add(data, addr, permission)
        import json
        data = json.loads(json.dumps(data))
        sorted(data.iteritems(), key=lambda x: x[1])
        return data

    def content_fuc(self, class_id):
        the_power = {
                'insert': False,
                'modify': False,
                'remove': False,
                'review': False
            }
        if 'ContentMod' in self.allow_fuc:
            for n in ['insert', 'modify', 'remove', 'review']:
                if n in self.allow_fuc['ContentMod']:
                    if class_id in self.allow_fuc['ContentMod'][n]:
                        the_power[n] = True
        return the_power
        pass

if __name__ == '__main__':
    from core.user import User
    # super = User(ident='super', pwd='superadmin')
    # user = User(ident='lalala', pwd='nashishenmegui')
    # print CMSFrame(super).allow_fuc
    # print CMSFrame(super).content_fuc('1-1')
    # print CMSFrame(user).allow_fuc
    # import json
    # print json.dumps(CMSFrame(super).allow_column, indent=2)
    pass
