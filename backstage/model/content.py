# coding=utf-8
import json
__author__ = 'dolacmeo'
__doc__ = ''


class ContentModel:
    def __init__(self, user_info=None):
        from core.user import User
        if isinstance(user_info, User):
            self.user = user_info
            if not self.user.is_login:
                raise Exception('Login first')

    def data_format(self, form_data, class_id):
        from core import CMS
        data = json.loads(json.dumps(form_data))
        tmp = CMS.setting_info('content')[CMS.column_info({'class_id': class_id})['type']]


if __name__ == '__main__':
    pass
