# coding=utf-8
from flask import Flask, request, redirect
from flask_restplus import Namespace, Resource, fields, Model
from .model import APIModel
import json

__author__ = 'dolacmeo'
__doc__ = ''

column_api = Namespace('column', description="文章系统接口")

column_content_parser = column_api.parser()
column_content_parser.add_argument('apikey', type=str, required=True, help='APIkey', location='args')
column_content_parser.add_argument('limit', type=str, required=True, help='查找数量', location='args', default='10')
column_content_parser.add_argument('skip', type=str, required=True, help='略过数量', location='args', default='0')
column_content_parser.add_argument('is_reviewed', type=bool, required=True, help='审核通过', location='args', default=True)

column_data = column_api.model('ContentData',
                               {'_id': fields.String(required=True, description='文章id',
                                                     example='57d7aa0e0b05551c84c48a55'),
                                'reviewed': fields.Boolean(required=True, description='审核状态', example=True),
                                'status': fields.String(required=True, description='状态', example='normal'),
                                'statistics': fields.String(required=True, description='统计数据', example='{}'),
                                'title': fields.String(required=True, description='文章标题', example='测试文章abcdefgf'),
                                'class_id': fields.String(required=True, description='分类id', example='1-2'),
                                'content_type': fields.String(required=True, description='文章类型', example='article'),
                                'addtime': fields.String(required=True, description='发布时间', example='2016-06-06')})

column_content_response = column_api.model('ColumnContent', {
    'success': fields.Boolean(required=True, description='成功标识', example=True),
    'error': fields.String(required=False, description='错误信息', example=''),
    'data': fields.List(fields.Nested(column_data))
})


@column_api.route('/<class_id>')
@column_api.param('class_id', '分类id', default='1-1')
@column_api.response(201, '操作成功')
@column_api.response(406, '验证失败')
class ColumnContent(Resource):
    @column_api.doc('用户登录', parser=column_content_parser)
    @column_api.marshal_with(column_content_response, code=201)
    def get(self, class_id):
        """支付宝异步通知接口
        """
        data = json.loads(json.dumps(request.args))
        if 'apikey' not in data:
            return {'success': False, 'error': 'Need input apikey', 'data': []}
        return APIModel(apikey=data['apikey']).column().get_list(class_id,
                                                                 limit=int(data['limit']),
                                                                 skip=int(data['skip']),
                                                                 is_reviewed=data['is_reviewed'])
