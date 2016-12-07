# coding=utf-8
import json
import os
from flask import Blueprint, render_template, request, session, redirect, Response, abort
from model import CMSModel as model
from core import CMS

__author__ = 'dolacmeo'
__doc__ = ''

backstage = Blueprint('backstage', __name__, template_folder='templates')

URL_BASE = '/control'
BASE_DIR = os.path.dirname(backstage.root_path)


def frame_data(user_model):
    base_data = user_model.base_data
    base_data.update(username=session.get('username', '未登录'),
                     URL_BASE=URL_BASE)
    base_data.update(api_func=CMS.setting_info('system')['api_func'])
    base_data.update(all_classid=CMS.setting_info('system')['all_column'])
    return base_data


@backstage.app_template_filter('fuc_name')
def get_fuc_name(fuc_name):
    if '#' in fuc_name:
        all_fuc = CMS.setting_info('system')['all_fuc']
        if fuc_name in all_fuc.keys():
            return all_fuc[fuc_name]
        else:
            return fuc_name
    else:
        all_fuc = CMS.setting_info('system')['fuc_name']
        if fuc_name in all_fuc.keys():
            return all_fuc[fuc_name]
        else:
            return fuc_name


@backstage.app_template_filter('id2username')
def id2username(user_id):
    return model().filter.username(user_id)


@backstage.app_template_filter('id2content_title')
def id2content_title(content_id):
    return model().filter.content_title(content_id)


@backstage.app_template_filter('is_dict')
def is_dict(item):
    return isinstance(item, dict)


@backstage.app_template_filter('column_name')
def get_column_name(column_id):
    return CMS.column_info({'class_id': column_id})['title']


@backstage.app_template_filter('column_type')
def get_column_name(column_id):
    return CMS.column_info({'class_id': column_id})['type']


@backstage.app_template_filter('show_type')
def show_type(item):
    return str(type(item))[7:-2]


@backstage.route(URL_BASE + '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        from backstage.tools.vaildata import generate_authenticode as gen
        code, img_tag = gen()
        session['code'] = code
        return render_template('backstage/login.html',
                               URL_BASE=URL_BASE, img_tag=img_tag)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if request.form['code'].lower() == session['code'].lower():
            m = model(ident=username, pwd=password).user
            if m.is_login:
                if m.permission or m.group == 'super':
                    session['is_login'] = True
                    session['username'] = username
                    session['password'] = password
                    del session['code']
                    return redirect(URL_BASE + '/home')
                else:
                    return json.dumps({'success': False, 'error': 'Need Permission'})
            else:
                return json.dumps({'success': False, 'error': 'Login Fail'})
        else:
            return json.dumps({'success': False, 'error': 'code error'})


@backstage.route(URL_BASE + '/logout', methods=['GET', 'POST'])
def logout():
    for n in session.keys():
        del session[n]
    return redirect(URL_BASE + '/login')


@backstage.route(URL_BASE + '/home', methods=['GET', 'POST'])
def index():
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    return render_template('backstage/index.html', **frame_data(user))


@backstage.route(URL_BASE + '/model/<mod>', methods=['GET', 'POST'])
def models(mod):
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    ident = session["username"]
    pwd = session["password"]
    if request.method == 'POST':
        return ""
    elif request.method == 'GET':  # 请求带参，自动生成带参路由
        xx = request.args
        print request.args
        search_data = dict(limit=int(request.args['limit']) if 'limit' in request.args else 10,
                           skip=int(request.args['skip']) if 'skip' in request.args else 0,
                           ident=request.args['ident'] if 'ident' in request.args and
                                                          json.loads(request.args['ident']) != {} else {})
        list_data = user.method(mod_name=mod, fuc_name='get_list', **search_data)
        search_data['total'] = list_data.get('total', 10)
        search_data['base_url'] = URL_BASE + '/model/%s' % mod
        search_data['query'] = ('&ident=' + json.dumps(search_data['ident'])) if json.loads(
            json.dumps(search_data['ident'])) else ''
        return render_template('backstage/models.html', page_model=mod,
                               content_title=CMS.setting_info('system')['fuc_name'][mod],
                               content_page='/%s.html' % mod,
                               content_power=user.frame.content_fuc("1-1"),
                               list_data=list_data, page=search_data,
                               **frame_data(user))
    else:
        return ""


@backstage.route(URL_BASE + '/model/<mod>/detail', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def models_detail(mod):
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    if request.method == 'GET':
        print request.args
        if 'id' not in request.args:
            return "ERROR: args without id"
        return render_template('backstage/models.html', page_model=mod,
                               content_title=CMS.setting_info('system')['fuc_name'][mod],
                               content_page='/%s_detail.html' % mod,
                               data_detail=user.method(mod_name=mod, fuc_name='details',
                                                       _id=request.args['id'] if 'id' in request.args else None),
                               **frame_data(user))
    elif request.method == 'POST':
        print request.form
        update_data = json.loads(json.dumps(request.form))
        fuc_name = update_data['fuc_name']
        del update_data['fuc_name']
        result = user.method(mod_name=mod, fuc_name=fuc_name, **update_data)
        return result
    elif request.method in ['PATCH', 'DELETE']:
        print request.values
        update_data = json.loads(json.dumps(request.values))
        fuc_name = update_data['fuc_name']
        del update_data['fuc_name']
        result = user.method(mod_name=mod, fuc_name=fuc_name, **update_data)
        return result
    else:
        return abort(403)



@backstage.route(URL_BASE + '/column/<class_id>', methods=['GET', 'POST'])
def column(class_id):
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    if request.method == 'POST':
        print request.form
        datas = json.loads(request.form['datas'])
        fuc = request.form['fuc']
        return user.method(mod_name='ContentMod', fuc_name=fuc,
                           params={'class_id': class_id}, datas=datas)
    elif request.method == 'GET':
        print request.args
        column_info = CMS.column_info({'class_id': class_id})
        temp = CMS.setting_info('content')['content_default'][column_info['type']]['data']
        if column_info['type'] + '.html' in user.base.get_column_html(BASE_DIR):
            content_page = '/column/' + column_info['type'] + '.html'
        else:
            content_page = '/column_content.html'
        search_data = dict(limit=int(request.args['limit']) if 'limit' in request.args else 10,
                           skip=int(request.args['skip']) if 'skip' in request.args else 0,
                           ident=request.args['ident'] if 'ident' in request.args and
                                                          json.loads(request.args['ident']) != {} else {})
        search_data['ident'].update({'class_id': class_id})
        list_data = user.method(mod_name='ContentMod', fuc_name='get_list', **search_data)
        return render_template('backstage/column.html', list_data=list_data, class_id=class_id,
                               temp=temp, father=column_info['father'],
                               content_title='内容管理: ' + CMS.column_info({'class_id': class_id})['title'],
                               content_power=user.frame.content_fuc(class_id),
                               content_page=content_page,
                               **frame_data(user))


@backstage.route(URL_BASE + '/sys-setup', methods=['GET', 'POST'])
def system_setting():
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    return render_template('backstage/models.html',
                           content_page='/SystemSetting.html',
                           **frame_data(user))


@backstage.route(URL_BASE + '/user-setup', methods=['GET', 'POST'])
def user_setting():
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    if request.method == 'POST':
        the_data = json.loads(request.form['info_data'])
        is_update = user.user.info_update(info=the_data)
        return json.dumps(is_update)
    elif request.method == 'GET':
        return render_template('backstage/models.html',
                               content_page='/UserSetting.html',
                               **frame_data(user))


@backstage.route(URL_BASE + '/file_upload', methods=['GET', 'POST'])
def file_upload():
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    if request.method == 'GET':
        return '''
<!doctype html>
<html>
<body>
<form action='/control/file_upload' method='post' enctype='multipart/form-data'>
 <input type='file' name='fileList'>
 <input type='submit' value='Upload'>
</form>
'''
    elif request.method == 'POST':
        f = request.files['fileList']
        db_data = CMS.FileService().save(f)
        return db_data['sha1']


@backstage.route(URL_BASE + '/file_list', methods=['POST'])
def file_list():
    if not session.get('is_login', False):
        return redirect(URL_BASE + '/login')
    user = model(ident=session['username'], pwd=session['password'])
    return CMS.FileService().file_list(json.loads(json.dumps(request.form)), return_type='str')


@backstage.route(URL_BASE + '/img/<img_sha1>', methods=['GET'])
def file_load(img_sha1):
    user = model(ident=session['username'], pwd=session['password'])
    try:
        the_file = CMS.FileService().load(img_sha1)
        if not the_file['success']:
            return the_file['error']
        if request.headers.get('If-Modified-Since') == the_file['time'].ctime():
            return Response(status=304)
        resp = Response(the_file['data'], mimetype='image/' + the_file['mime'])
        resp.headers['Last-Modified'] = the_file['time'].ctime()
        return resp
    except Exception, e:
        print e
        abort(404)


@backstage.route('/test')
def test_page():
    user = model(ident=session['username'], pwd=session['password'])
    return render_template('backstage/test.html', **frame_data(user))


if __name__ == '__main__':
    # print backstage.root_path
    pass
