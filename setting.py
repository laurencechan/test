# coding=utf-8
__author__ = 'dolacmeo'
__doc__ = '配置文件'


class ContentType:
    article = {"content_type": "article",
               "data": {
                   "content": "str,文章内容,这是一段普通的测试内容",
                   "title": "str,文章题目,测试文章",
                   "author_name": "str,作者名字,我是谁",
                   "author_id": "str,作者ID,57ce5af90b0555043c60e7d9",
                   "from": "str,文章来源,火星",
                   "thumbnail": "str,头图,http://ajcreative.net/wp-content/uploads/2014/12/blog-head.jpg",
                   "images": [{
                       "img_src": "str,图片地址,https://www.baidu.com/img/baidu_jgylogo3.gif",
                       "description": "str,图片描述,这是百度logo",
                       "url_to": "str,图片链接,https://www.baidu.com/"
                   }]}}
    html_page = {"content_type": "html_page",
                 "data": {
                     "html": 'str,页面源码,'
                             '<!DOCTYPE html><html><head><title>Test Title</title></head>'
                             '<body><h1>Hello World</h1></body></html>',
                     "title": "str,页面题目,测试页面",
                     "author_name": "str,作者名字,我是谁",
                     "author_id": "str,作者ID,57ce5af90b0555043c60e7d9",
                     "from": "str,文章来源,火星",
                     "thumbnail": "str,头图,http://ajcreative.net/wp-content/uploads/2014/12/blog-head.jpg"
                 }}
    album = {"content_type": "album",
             "data": {
                 "content": "str,相册简介,老司机就要发车了",
                 "title": "str,相册标题,一言不合就发车",
                 "author_name": "str,作者名字,我是谁",
                 "author_id": "str,作者ID,57ce5af90b0555043c60e7d9",
                 "from": "str,文章来源,火星",
                 "thumbnail": "str,头图,http://ajcreative.net/wp-content/uploads/2014/12/blog-head.jpg",
                 "images": [{
                     "img_src": "str,图片地址,https://www.baidu.com/img/baidu_jgylogo3.gif",
                     "description": "str,图片描述,这是百度logo",
                     "url_to": "str,图片链接,https://www.baidu.com/"
                 }]}}
    video = {"content_type": "video",
             "data": {
                 "html": 'str,页面源码,'
                         '<!DOCTYPE html><html><head><title>Test Title</title></head>'
                         '<body><h1>Hello World</h1></body></html>',
                 "title": "str,视频标题,突然发车啦",
                 "author_name": "str,作者名字,我是谁",
                 "author_id": "str,作者ID,57ce5af90b0555043c60e7d9",
                 "from": "str,文章来源,火星",
                 "thumbnail": "str,头图,http://ajcreative.net/wp-content/uploads/2014/12/blog-head.jpg"}}
    exam_data = {"content_type": "exam_data",
                 "data": {
                     "data_type": "str,题目类型,选择题",
                     "content": "str,试题内容,大象放冰箱一共分几步",
                     "option": "str,选项,[A]|B|[C]|D",
                     "author_id": "str,作者ID,57ce5af90b0555043c60e7d9"
                 }}
    exam_test = {"content_type": "exam_test",
                 "data": {
                     "subs": [{
                         "name": "str,试题类型,单选题",
                         "tests": [{
                             "id": "str,试题ID,uqweojrlaskdlnvln",
                             "value": "int,分值,5",
                             "data": {}
                         }]}],
                     "test_type": "str,测验类型,城区竞赛",
                     "subject": "str,测验标题,共产党咋样",
                     "author_id": "str,作者ID,57ce5af90b0555043c60e7d9",
                     "scores": "int,总分数,100"
                 }}
    profile = {"content_type": "profile",
               "data": {
                   "content": "str,个人简介,这是一个好人",
                   "name": "str,姓名,我是谁",
                   "sex": "str,性别,男",
                   "birth": "str,出生日期,1999-09-09",
                   "organization": "str,所在单位,什么局",
                   "photo": "str,个人照片,http:///",
                   "join_party": "datetime,,",
                   "left_party": "datetime,,",
                   "honor": "str,获得荣誉,好像得过什么奖",
                   "duty": "str,工作岗位,上班打更"
               }}


class ProjectMod:
    regmod = {
        'UserMod#create': '创建用户',
        'UserMod#reset_pwd': '重置密码',
        'UserMod#modify': '修改用户',
        'UserMod#details': '用户详情',
        'UserMod#get_list': '用户列表',

        'PermissionMod#grant': '用户授权',
        'PermissionMod#revoke': '反授权',
        'PermissionMod#remove_model': '删除权限模板',
        'PermissionMod#setup_model': '维护权限模板',
        'PermissionMod#details': '权限详情',
        'PermissionMod#get_list': '用户权限列表',

        'ContentMod#insert': '新增文章',
        'ContentMod#modify': '修改文章',
        'ContentMod#remove': '删除文章',
        'ContentMod#details': '文章详情',
        'ContentMod#get_list': '查找文章',
        'ContentMod#review': '文章审核',

        'CommentMod#add': '添加评论',
        'CommentMod#remove': '删除评论',
        'CommentMod#modify': '修改评论',
        'CommentMod#details': '评论详情',
        'CommentMod#get_list': '获取评论',
        'CommentMod#review': '评论审核',

        'PushMod#get_list': '推送列表',
        'PushMod#push': '推送通知',
    }
    modlist = {'UserMod': '用户系统',
               'PermissionMod': '权限系统',
               'ContentMod': '内容管理',
               'CommentMod': '评论管理',
               'PushMod': '推送消息'
               }
    for n in regmod.keys():
        if n.split('#')[0] not in modlist.keys():
            modlist[n.split('#')[0]] = n.split('#')[0]
    support_content = [n for n in ContentType.__dict__.keys() if n[0] != '_']


class UserSetting:
    # 默认用户表结构default不能更改, 可对补充信息info做自定义
    default = {
        "username": "default",
        "password": "password",
        "phone": "",
        "permission": {
            "group": "user",
            "tag": {}
        }
    }
    info = {
        "infos": {
            "sex": "",
            "age": "",
            "headimg": "",
            "belong": ""
        },
        "status": {
            "score": {},
            "device_info": {"id": ""}
        }
    }
    default.update(info)


class Column:
    # 至多三级类目
    ColumnTree = {
        '1': {'title': '党建之魂', 'subject': '', 'type': 'column'},
        '1-1': {'title': '中央决策',
                'subject': '党章、党规及中央有关党建规定、决策、条例、要求', 'type': 'article'},
        '1-2': {'title': '习总书记系列讲话',
                'subject': '习总书记重要讲话和论述', 'type': 'article'},
        '1-3': {'title': '省委要求',
                'subject': '省委落实中央决策有关意见、要求和布置', 'type': 'article'},
        '1-4': {'title': '领导讲话',
                'subject': '省领导及工委主要领导有关党建工作的讲话', 'type': 'article'},
        '1-5': {'title': '工委部署',
                'subject': '工委落实中央和省委决策意见的工作部署', 'type': 'article'},
        '2': {'title': '党建视窗', 'subject': '', 'type': 'column'},
        '2-1': {'title': '厅局快讯',
                'subject': '厅局党建工作展示', 'type': 'article'},
        '2-2': {'title': '市（地）动态',
                'subject': '市（地）党建工作展示', 'type': 'article'},
    }


class Permission:
    super_pass = 'superadmin'
    ControlTree = {
        'super': {
            "instruction": "超级管理员",
            "group_name": "super",
            "is_top": True,
            "control": ["admin", "junior", "member", "user"]
        },
        'admin': {
            "instruction": "管理员",
            "group_name": "admin",
            "is_top": False,
            "control": ["junior", "member", "user"]
        },
        'junior': {
            "instruction": "基层管理员",
            "group_name": "junior",
            "is_top": False,
            "control": ["member", "user"]
        },
        'member': {
            "instruction": "基层党员",
            "group_name": "member",
            "is_top": False,
            "control": []
        },
        'user': {
            "instruction": "用户",
            "group_name": "user",
            "is_top": False,
            "control": []
        }
    }


class Mongodb_setup:
    user_name = 'master'
    pass_word = 'dbmaster'
    address = '125.211.222.237:27638'
    # address = '192.168.22.101:27638'
    db_name = 'db_CCPhlj_Building'

    # user_name = 'root'
    # pass_word = 'root'
    # address = 'localhost'
    # db_name = 'db_CCP'

    collections = {
        'Setting':
            {'remark': '项目设置',
             'init_data': []},
        'Permission':
            {'remark': '权限设置',
             'init_data': []},
        'User':
            {'remark': '用户表',
             'init_data': []},
        'Column':
            {'remark': '栏目分组表',
             'init_data': []},
        'Content':
            {'remark': '内容表',
             'init_data': []},
        'Comment':
            {'remark': '评论表',
             'init_data': []},
        'Push':
            {'remark': '推送表',
             'init_data': []},
        'Images':
            {'remark': '图片表',
             'init_data': []}
    }


if __name__ == '__main__':
    pass
