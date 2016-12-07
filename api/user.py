# coding=utf-8
from flask import Flask, request, redirect
from flask_restplus import Namespace, Resource, fields, Model
from .model import APIModel
import json

__author__ = 'dolacmeo'
__doc__ = ''

user_api = Namespace('user', description="用户系统接口")

user_login_parser = user_api.parser()
user_login_parser.add_argument('ident', type=str, required=True, help='登录名', location='form')
user_login_parser.add_argument('pwd', type=str, required=True, help='登录密码', location='form')
user_login_response = user_api.model('User_login', {
    'success': fields.Boolean(required=True, description='成功标识', example=True),
    '_id': fields.String(required=True, description='数据库id', example='57d3aeea0b05551588e1bae8'),
    'apikey': fields.String(required=True, description='apikey', example='FCA46A3D0EDD711037FC88C10CD1D0E1'),
    'error': fields.String(required=False, description='错误信息', example='')
})


@user_api.route('/login')
@user_api.response(201, '操作成功')
@user_api.response(406, '验证失败')
class UserLogin(Resource):
    @user_api.doc('用户登录', parser=user_login_parser)
    @user_api.marshal_with(user_login_response, code=201)
    def post(self):
        """用户登录 获取APIKEY
        """
        data = json.loads(json.dumps(request.form))
        if not ('ident' in data and 'pwd' in data):
            return {'success': False, '_id': '', 'apikey': '', 'error': 'Need input ident or pwd'}
        return APIModel(**data).user.set_apikey()

user_logout_parser = user_api.parser()
user_logout_parser.add_argument('apikey', type=str, required=True, help='APIkey', location='form')
user_logout_response = user_api.model('User_logout', {
    'success': fields.Boolean(required=True, description='成功标识', example=True),
    '_id': fields.String(required=True, description='数据库id', example='57d3aeea0b05551588e1bae8'),
    'apikey': fields.String(required=True, description='apikey', example='FCA46A3D0EDD711037FC88C10CD1D0E1'),
    'error': fields.String(required=False, description='错误信息', example='')
})


@user_api.route('/logout')
@user_api.response(201, '操作成功')
@user_api.response(406, '验证失败')
class UserLogout(Resource):
    @user_api.doc('退出登录', parser=user_logout_parser)
    @user_api.marshal_with(user_logout_response, code=201)
    def post(self):
        """退出登录 删除APIKEY
        """
        data = json.loads(json.dumps(request.form))
        if 'apikey' not in data:
            return {'success': False, '_id': '', 'apikey': '', 'error': 'Need input apikey'}
        return APIModel(apikey=data['apikey']).user.unset_apikey()
