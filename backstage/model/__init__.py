# coding=utf-8

__author__ = 'dolacmeo'
__doc__ = ''


class CMSModel:
    def __init__(self, **kwargs):
        if kwargs:
            from core.user import User
            self.user = User(**kwargs)
            self.base_data = dict(
                    all_fuc=self.frame.allow_fuc,
                    all_column=self.frame.allow_column
            )
        pass

    def method(self, mod_name, fuc_name, **kwargs):
        from core import CMS
        cms = CMS(self.user)
        return getattr(getattr(cms, mod_name)(), fuc_name)(**kwargs)

    @property
    def base(self):
        from .base import BaseFunc
        return BaseFunc(self.user)

    @property
    def frame(self):
        from .frame import CMSFrame
        return CMSFrame(self.user)

    @property
    def content(self):
        from .content import ContentModel
        return ContentModel(self.user)

    @property
    def filter(self):
        from .filter import Filter
        return Filter()

    @property
    def images(self):
        from core import CMS
        return CMS.FileService()

    pass


if __name__ == '__main__':
    pass
