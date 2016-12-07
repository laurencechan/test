# coding=utf-8
from core import CMS
from core.user import User
from backstage.model import CMSModel

super = CMS(User(ident='super', pwd='superadmin'))
# user = CMS(User(ident='lalala', pwd='nashishenmegui'))

data = {"content": "这是一段普通的测试内容啊啊啊啊啊啊啊啊",
        "title": "测试文章",
        "author_name": "作者名字",
        "author_id": "57ce5af90b0555043c60e7d9",
        "from": "文章来源火星",
        "thumbnail": "http://ajcreative.net/wp-content/uploads/2014/12/blog-head.jpg",
        "images": [{
            "img_src": "https://www.baidu.com/img/baidu_jgylogo3.gif",
            "description": "这是百度logo",
            "url_to": "https://www.baidu.com/"
        },
            {
                "img_src": "https://www.baidu.com/img/baidu_jgylogo3.gif",
                "description": "这是百度logo",
                "url_to": "https://www.baidu.com/"
            }
        ]}


def program_size(except_dir=None):
    if except_dir is None:
        except_dir = ['flask_restplus', 'jpush']
    sum_line = 0
    import os
    print os.getcwd()
    for root, dirs, files in os.walk(os.getcwd()):
        for fi in files:
            not_in = True
            for n in except_dir:
                if n in root:
                    not_in = False
                    break
            if fi.split('.')[1] == 'py' and not_in:
                with open(os.path.join(root, fi)) as f:
                    lines = f.readlines()
                    lines = list(set(lines))
                    if len(lines):
                        print os.path.join(root, fi), len(lines)
                    sum_line += len(lines)
    print sum_line
    return sum_line


def test_content(class_id='1-1', data=data, num='001'):
    data['title'] += num
    CMSModel(ident='super', pwd='superadmin').method('ContentMod', 'insert',
                                                     class_id=class_id, content_json=data)


def test_user(name, pwd):
    super.UserMod().create(username=name, password=pwd)

info = {
        "infos": {
            # "sex": "male",
            # "age": "28",
            # "headimg": "",
            # "belong": "KFC"
        },
        "status": {
            # "score": {},
            "device_info": {"id": "123456"}
        }
    }

if __name__ == '__main__':
    # for n in range(15):
    #     print n,
    #     test_content(num=str(n))
    # test_user()
    # super.user.info_update(info)
    # test_user('abcdefg', 'abcdefg123')
    # user = CMS(User(ident='abcdefg', pwd='abcdefg123'))
    # user.user.info_update(info)
    # import json
    # print json.dumps(info)
    # super.PermissionMod().grant('abcdefg', 'ContentMod#insert', ['1-1', '1-2'])
    # program_size()
    # print super.all_func
    print super.UserMod().create('rhewitt26654', 'ffwfafsdfas',phone='15265983264',group="user")
    pass
