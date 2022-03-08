from pymongo import MongoClient
import jwt
from jwt import encode
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://rlawlgh3894:test123!@cluster0.ktjzj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.makeCool


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/api/information')
def info():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})

        return render_template('information.html', id=user_info["id"], name=user_info["name"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/api/profile')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/api/profile/login', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/information', methods=['post'])
def api_information():
    token_receive = request.cookies.get('mytoken')
    idload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": idload['id']})

    id_receive = user_info["id"]
    password_receive = request.form['password_give']
    name_receive = request.form['name_give']
    age_receive = request.form['age_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 회원정보 확인후 암호화/토큰발행
    db.users.update_one({'id': id_receive}, {'$set': {'pw': pw_hash}, })
    db.users.update_one({'id': id_receive}, {'$set': {'name': name_receive}, })
    db.users.update_one({'id': id_receive}, {'$set': {'age': age_receive}, })
    # pymongo에 pw변경
    return jsonify({'result': 'success','msg': '정보변경 완료!'})


@app.route('/api/profile/regist', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    name_receive = request.form['name_give']
    gender_receive = request.form['gender_give']
    age_receive = request.form['age_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": username_receive,                                # 아이디
        "pw": password_hash,                                   # 비밀번호
        "name": name_receive,                                  # 이름
        "age": age_receive,                                    # 나이
        "gender": gender_receive,                              # 성별
        "like": "",                                            # 좋아요
        "favorite": ""                                         # 즐겨찾기
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/api/profile/regist/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/main')
def main():
    return render_template('main.html')


@app.route("/api/main/neck", methods=["GET"])
def necklist_get():
    list_neck = list(db.neck.find({}, {'_id': False}))
    return jsonify({'main_list': list_neck})


@app.route("/api/main/waist", methods=["GET"])
def waistlist_get():
    list_waist = list(db.waist.find({}, {'_id': False}))
    return jsonify({'main_list': list_waist})


@app.route("/api/main/wrist", methods=["GET"])
def wristlist_get():
    list_wrist = list(db.wrist.find({}, {'_id': False}))
    return jsonify({'main_list': list_wrist})


@app.route("/api/main/lowerBody", methods=["GET"])
def lowerBodylist_get():
    list_lowerBody = list(db.lowerBody.find({}, {'_id': False}))
    return jsonify({'main_list': list_lowerBody})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
