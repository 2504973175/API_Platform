import random

from flask import Flask, render_template, request, jsonify
import requests
from werkzeug.exceptions import abort

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', resp=None)

@app.route('/handle_get', methods=['POST'])
def handle_get():
    url = request.form['url']
    assertion = request.form['assert']
    assertion_success = None
    try:
        r = requests.get(url)
        if assertion is not None and assertion != '':
            obj = r.json() #获取响应的json对象给obj
            if assertion:
                assertion_success = eval(assertion) #返回都是true
    except Exception as e:
        print(e)
        r = None

    resp = build_resp(r)
    resp['assertion'] = assertion
    resp['assertion_success'] = assertion_success #只要写了就是true

    return render_template('home.html', resp=resp)
def build_resp(r):
    resp = {'success': False}
    if r is None:
        return resp

    if r.status_code < 400:
        resp['success'] = True

    resp['url'] = r.url
    resp['text'] = r.text
    resp['headers'] = r.headers
    resp['status_code'] = r.status_code

    return resp
# @app.route('/show')
# def show():
#     return resp 如何在页面之前传数据？
@app.route('/api')
def api():
    return jsonify({'name': 'etf', 'version': '0.01'})

@app.route('/error') #相当于造了一个错误的接口
def error():
    codes = [404, 401, 403, 500]
    random.shuffle(codes)
    abort(codes[0])
if __name__ == '__main__':
   app.run(debug=True)