# coding=utf-8

__author__ = 'dolacmeo'
__doc__ = ''


class ClassTool:
    def __init__(self):
        # self.mod_fuc = [self.__class__.__name__+'#'+n for n in dir(self.__class__) if n[0] != '_']
        pass

    def __getattr__(self, item):
        if item == 'fuc':
            return [self.__class__.__name__+'#'+n for n in dir(self.__class__) if n[0] != '_']
        # else:
        #     return getattr(self, item)

    def _get_fuc_name(self):
        import sys
        return self.__class__.__name__ + '#' + sys._getframe().f_back.f_code.co_name

    def _sys_msg(self, success, error='', ext_json=None):
        import sys
        msg = dict(
            success=True if success else False,
            error_info=error if not success else '',
            fuc_name=self.__class__.__name__ + '#' + sys._getframe().f_back.f_code.co_name,
        )
        if isinstance(success, dict) or isinstance(success, list):
            msg.update({'data': success if success else None})
        if isinstance(ext_json, dict):
            msg.update(ext_json)
        return msg

    pass


if __name__ == '__main__':
    pass
