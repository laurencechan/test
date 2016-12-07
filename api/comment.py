# coding=utf-8
from flask import Flask, request, redirect
from flask_restplus import Namespace, Resource, fields, Model
from .model import APIModel
import json

__author__ = 'dolacmeo'
__doc__ = ''

comment_api = Namespace('comment', description="评论系统接口", default_mediatype='text/plain')

comment_get_parser = comment_api.parser()
comment_get_parser.add_argument('apikey', type=str, required=True, help='APIkey', location='args')

comment_data = comment_api.model('CommentData',
             {'_id': fields.String(required=True, description='评论id', example='57d3a649ea6901070a28264f'),
              'main_id': fields.String(required=True, description='关联文章id', example='57d0e3f30b055524c00e71ca'),
              'level_num': fields.Integer(required=True, description='楼层数', example=1),
              'level_reply': fields.Integer(required=True, description='回复楼层', example=''),
              'content': fields.String(required=True, description='评论内容', example='这是评论这是评论'),
              'username': fields.String(required=True, description='用户名', example='username'),
              'user_id': fields.String(required=True, description='用户id', example='57d3afcefb98a4878190d517'),
              'reviewed': fields.Boolean(required=True, description='已审核', example=True)})

comment_get_response = comment_api.model('GetComment', {
    'success': fields.Boolean(required=True, description='成功标识', example=True),
    'error': fields.String(required=False, description='错误信息', example=''),
    'data': fields.List(fields.Nested(comment_data))
})

comment_post_parser = comment_api.parser()
comment_post_parser.add_argument('apikey', type=str, required=True, help='APIkey', location='form')
comment_post_parser.add_argument('comment', type=str, required=True, help='评论内容', location='form')
comment_post_parser.add_argument('level_reply', type=str, required=False, help='回复楼层', location='form')

comment_post_response = comment_api.model('PostComment', {
    'success': fields.Boolean(required=True, description='成功标识', example=True),
    'error': fields.String(required=False, description='错误信息', example=''),
    '_id': fields.String(required=False, description='评论id', example='57d3a649ea6901070a28264f')
})


@comment_api.route('/<content_id>')
@comment_api.param('content_id', '关联文章id', default='57d0e3f30b055524c00e71ca')
@comment_api.response(201, '操作成功')
@comment_api.response(406, '验证失败')
class UserComment(Resource):
    @comment_api.doc('获取评论', parser=comment_get_parser)
    @comment_api.marshal_with(comment_get_response, code=200)
    def get(self, content_id):
        """根据文章id获取相关评论
        """
        data = json.loads(json.dumps(request.args))
        if 'apikey' not in data:
            return {'success': False, 'error': 'Need input apikey', 'data': []}
        return APIModel(apikey=data['apikey']).comment().get_comment(content_id)

    @comment_api.doc('发表评论', parser=comment_post_parser)
    @comment_api.marshal_with(comment_post_response, code=200)
    def post(self, content_id):
        """根据文章id发表评论
        """
        data = json.loads(json.dumps(request.form))
        if 'apikey' not in data:
            return {'success': False, 'error': 'Need input apikey', 'data': []}
        return APIModel(apikey=data['apikey']).comment().add_comment(content_id, comment=data['comment'],
                                                     level_reply=data['level_reply'] if 'level_reply' in data else None)
