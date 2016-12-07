# coding=utf-8
from flask import Blueprint
from flask_restplus import Api
from .user import user_api
from .column import column_api
from .comment import comment_api
from .content import content_api

__author__ = 'dolacmeo'
__doc__ = ''

description = """
- - -
 """

blueprint = Blueprint('cms_api', __name__, url_prefix='/interface')
cms_api = Api(blueprint,
              validate=False,
              version='1.0',
              title="CMS管理系统接口文档",
              description=description,
              contact='dolacmeo@qq.com')

cms_api.add_namespace(user_api)
cms_api.add_namespace(column_api)
cms_api.add_namespace(comment_api)
cms_api.add_namespace(content_api)

if __name__ == '__main__':
    pass
