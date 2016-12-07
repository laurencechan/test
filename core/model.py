# coding=utf-8
from conn import MongoHelp

__author__ = 'dolacmeo'
__doc__ = '模块装饰器'
setting_conn = MongoHelp('Setting')

is_super_disable = setting_conn.find_one({'set_type': 'system'})['super_user']['disable']
func_registered = setting_conn.find_one({'set_type': 'system'})['all_fuc'].keys()


def ModVerify(func):
    """
    验证用户权限，处理数据结果，注册功能模块
    :param func:
    """
    content_less_permission = ['UserMod', 'PermissionMod']

    def wrapper(*args, **kwargs):
        if len(args) == 0:
            raise Exception('Used within class.func')
        user_model = args[0].user
        class_name = args[0].__class__.__name__
        fuc_name = args[0].__class__.__name__ + '#' + func.__name__
        print '%s:' % fuc_name
        if not user_model.is_login:
            raise Exception('Need User login first')
        if (fuc_name in user_model.permission.keys()) \
                or (user_model.group == 'super' and not is_super_disable):
            if user_model.group == 'super':
                return func(*args, **kwargs)
            if class_name not in content_less_permission:
                req_permission = args[0].req_permisssion
                if fuc_name not in user_model.permission.keys():
                    return {'success': False, 'error': 'Need permission %s' % fuc_name}
                if req_permission is not None and req_permission not in user_model.permission[fuc_name]:
                    return {'success': False, 'error': 'Need permission %s' % req_permission}
            return func(*args, **kwargs)
        else:
            return {'success': False, 'error': 'Need permission'}

    return wrapper


if __name__ == '__main__':
    pass
