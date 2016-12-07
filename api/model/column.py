# coding=utf-8
from core import CMS

__author__ = 'dolacmeo'
__doc__ = ''


class ColumnApi:
    def __init__(self, User_info=None):
        from core.user import User
        if isinstance(User_info, User):
            self.user = User_info

    def get_list(self, class_id, limit=10, skip=0, is_reviewed=True):
        if is_reviewed:
            ident = {"reviewed": True, "class_id": class_id}
        else:
            ident = {"class_id": class_id}
        return CMS(self.user).ContentMod().get_list(ident, limit, skip)

    def get_content(self, content_id):
        return CMS(self.user).ContentMod().details(content_id)

if __name__ == '__main__':
    pass
