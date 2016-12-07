# coding=utf-8
import datetime
import json
from conn import MongoHelp
from tools.py_class import ClassTool
import core.tools.jpush as jpush
from core.tools.jpush import common
from model import ModVerify

__author__ = 'dolacmeo'
__doc__ = ''

app_key = 'e7a775fb0d4b78927ef2aee9'
master_secret = '0ebeb2fe00f50f1d20586b4c'


class PushMod(ClassTool):
    def __init__(self, user_info=None):
        ClassTool.__init__(self)
        self.__conn = MongoHelp('Push')
        from user import User
        if isinstance(user_info, User):
            self.user = user_info
            self._push = jpush.JPush(app_key, master_secret).create_push()

    def push(self, id, title):

        self._push.audience = jpush.all_
        push_time = datetime.datetime.now()
        notification = {"extras": {"_id": str(id), "push_time": push_time.strftime('%Y-%m-%d %H:%M:%S')},
                        "alert": title}
        self._push.notification = jpush.notification(android=jpush.android(**notification),
                                                     ios=jpush.ios(**notification))
        self._push.platform = jpush.all_
        try:
            response = self._push.send()
            self._add(id, title, push_time, str(response).replace("Response Payload: ", ""), 1)
        except common.Unauthorized:
            self._add(id, title, push_time, "Unauthorized", 0)
        except common.APIConnectionException:
            self._add(id, title, push_time, "conn", 0)
        except common.JPushFailure, e:
            self._add(id, title, push_time, e.message, 0)
        except Exception, e:
            self._add(id, title, push_time, e.message, 0)

    @ModVerify
    def get_list(self, ident=None, limit=10, skip=0):
        if ident is None:
            ident = {}
        found = self.__conn.conn.find(ident).limit(limit).skip(skip)
        total = found.count()
        push_data = self.__conn.id_format(found)
        return self._sys_msg(push_data, 'Grant Fail', {'page': {'total': total, 'limit': limit, 'skip': skip}})

    def _add(self, content_id, title, push_time, callback, status=0):
        push_post = dict(
            platform={"content_id": content_id,
                      "title": title,
                      "push_time": push_time,
                      "push_person": self.user.user_data["_id"]},
            status=status,
            callback=json.loads(json.dumps(callback))
        )
        self.__conn.insert(push_post)


if __name__ == '__main__':
    print PushMod().fuc
    pass
