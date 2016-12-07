# coding=utf-8
from flask import Flask, request, redirect
from flask_restplus import Namespace, Resource, fields, Model
from .model import APIModel
import json

__author__ = 'dolacmeo'
__doc__ = ''

content_api = Namespace('content', description="文章系统接口", default_mediatype='text/plain')

content_content_parser = content_api.parser()
content_content_parser.add_argument('apikey', type=str, required=True, help='APIkey', location='args')

content_data = content_api.model('ContentData',
                                 {'_id': fields.String(required=True, description='文章id',
                                                       example='57d7aa0e0b05551c84c48a55'),
                                  'status': fields.String(required=True, description='审核状态', example='unreviewed'),
                                  'statistics': fields.String(required=True, description='统计数据', example='{}'),
                                  'title': fields.String(required=True, description='文章标题', example='测试文章abcdefgf'),
                                  'class_id': fields.String(required=True, description='分类id', example='1-2'),
                                  'content_type': fields.String(required=True, description='文章类型', example='article'),
                                  'addtime': fields.String(required=True, description='发布时间', example='2016-06-06'),
                                  'data': fields.String(example='{}')})

content_content_response = content_api.model('ColumnContent', {
    'success': fields.Boolean(required=True, description='成功标识', example=True),
    'error': fields.String(required=False, description='错误信息', example=''),
    'data': fields.Nested(content_data)
})


@content_api.route('/<content_id>')
@content_api.param('content_id', '文章id', default='57d7aa0e0b05551c84c48a55')
@content_api.response(201, '操作成功')
@content_api.response(406, '验证失败')
class ColumnContent(Resource):
    @content_api.doc('获取文章详情', parser=content_content_parser)
    @content_api.marshal_with(content_content_response, code=201)
    def get(self, content_id):
        """通过文章id 获取文章详情
        """
        data = json.loads(json.dumps(request.args))
        if 'apikey' not in data:
            return {'success': False, 'error': 'Need input apikey', 'data': []}
        return APIModel(apikey=data['apikey']).column().get_content(content_id)
