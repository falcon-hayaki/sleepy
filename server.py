#!/usr/bin/python3
# coding: utf-8
from datetime import datetime

import utils as u
from data import data as data_init
from flask import Flask, render_template, request, url_for, redirect, flash, make_response, jsonify
from markupsafe import escape


d = data_init()
app = Flask(__name__)

# ---


def reterr(code, message):
    ret = {
        'success': False,
        'code': code,
        'message': message
    }
    u.error(f'{code} - {message}')
    return u.format_dict(ret)


def showip(req, msg):
    ip1 = req.remote_addr
    try:
        ip2 = req.headers['X-Forwarded-For']
        u.infon(f'- Request: {ip1} / {ip2} : {msg}')
    except:
        ip2 = None
        u.infon(f'- Request: {ip1} : {msg}')


@app.route('/')
def index():
    showip(request, '/')
    web_data = get_data()
    return render_template(
        'index.html',
        **web_data
    )

@app.route('/refresh')
def refresh():
    web_data = get_data()
    return jsonify(web_data)
    
def get_data():
    d.load()
    ot = d.data['other']
    try:
        stat = d.data['status_list'][d.data['status']]
        if(d.data['status'] == 0):
            app_name = d.data['app_name']
            stat['name'] = app_name
    except:
        stat = {
            'name': '未知',
            'desc': '未知的标识符，可能是配置问题。',
            'color': 'error'
        }
    # 计时
    try:
        update_time = datetime.strptime(d.data.get('update_time', ''), u.TIME_FORMAT)
        record_time = (datetime.now() - update_time).total_seconds()
    except:
        record_time = -1
    return dict(
        user=ot['user'],
        learn_more=ot['learn_more'],
        repo=ot['repo'],
        status_name=stat['name'],
        status_desc=stat['desc'],
        status_color=stat['color'],
        more_text=ot['more_text'],
        record_time=record_time
    )

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/style.css')
def style_css():
    response = make_response(render_template(
        'style.css',
        bg=d.data['other']['background'],
        alpha=d.data['other']['alpha']
    ))
    response.mimetype = 'text/css'
    return response


@app.route('/query')
def query():
    d.load()
    showip(request, '/query')
    st = d.data['status']
    # stlst = d.data['status_list']
    try:
        stinfo = d.data['status_list'][st]
        if(st == 0):
            stinfo['name'] = d.data['app_name']
    except:
        stinfo = {
            'status': st,
            'name': '未知'
        }
    ret = {
        'success': True,
        'status': st,
        'info': stinfo
    }
    return u.format_dict(ret)


@app.route('/get/status_list')
def get_status_list():
    showip(request, '/get/status_list')
    stlst = d.dget('status_list')
    return u.format_dict(stlst)


@app.route('/set')
def set_normal():
    showip(request, '/set')
    status = escape(request.args.get("status"))
    app_name = escape(request.args.get("app_name"))
    try:
        status = int(status)
    except:
        return reterr(
            code='bad request',
            message="argument 'status' must be a number"
        )
    secret = escape(request.args.get("secret"))
    u.info(f'status: {status}, name: {app_name}, secret: "{secret}"')
    secret_real = d.dget('secret')
    if secret == secret_real:
        d.dset('status', status)
        d.dset('app_name', app_name)
        d.dset('update_time', datetime.now().strftime(u.TIME_FORMAT))
        u.info('set success')
        ret = {
            'success': True,
            'code': 'OK',
            'set_to': status,
            'app_name':app_name
        }
        return u.format_dict(ret)
    else:
        return reterr(
            code='not authorized',
            message='invaild secret'
        )



if __name__ == '__main__':
    d.load()
    app.run(
        host=d.data['host'],
        port=d.data['port'],
        debug=d.data['debug']
    )
