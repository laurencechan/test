# coding=utf-8
from flask import Flask
from backstage.home import backstage
from website.index import website
from api import blueprint as cms_api
from werkzeug.contrib.fixers import ProxyFix

import sys

__author__ = 'dolacmeo'
__doc__ = ''

# 强制支持UTF8编码
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['DEBUG'] = True
app.register_blueprint(backstage)
app.register_blueprint(website)
app.register_blueprint(cms_api)


app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

app.secret_key = '3PG#P*[UQrLdca9/'


if __name__ == '__main__':
    app.run()
    pass
