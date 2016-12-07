# coding=utf-8
import os
from flask import Blueprint, render_template, request, session, redirect

__author__ = 'dolacmeo'
__doc__ = ''

website = Blueprint('website', __name__, template_folder='templates')

URL_BASE = ''
BASE_DIR = os.path.dirname(website.root_path)


@website.route(URL_BASE + '/', methods=['GET', 'POST'])
def index():
    return """
    <a href='/control/home'>后台首页</a>
    <a href='/interface'>API接口</a>
    """

if __name__ == '__main__':
    pass
