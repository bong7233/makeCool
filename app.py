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

client = MongoClient(
    'mongodb+srv://rlawlgh3894:test123!@cluster0.ktjzj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.makeCool


@app.route('/')
def home():
    return render_template('login.html')


# 로그인한 유저 토큰검증 후 아이디 일치하는경우 index.html로 유저정보 전달
@app.route('/main')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        doc = {
            'name': user_info['name'],
            'id': user_info['id'],
            'like': user_info['like'],
            'favorite': user_info['favorite']
        }

        return render_template('index.html', user_info=doc, name=user_info['name'])

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 로그인한 유저 토큰검증 후 아이디 일치하는경우 favorite.html로 유저정보 전달
@app.route('/favorite')
def favorite_home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        doc = {
            'name': user_info['name'],
            'id': user_info['id'],
            'like': user_info['like'],
            'favorite': user_info['favorite']
        }

        return render_template('favorite.html', user_info=doc, name=user_info['name'])

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 즐겨찾기 비디오 불러오기
@app.route("/api/videos/favorite", methods=["GET"])
def videos_p():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = (db.users.find_one({"id": payload['id']})['like'])

        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", 'favorites': user_info})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
    
    
# 로그인한 유저 토큰검증 후 아이디 일치하는경우 information.html로 유저정보 전달
@app.route('/api/information')
def info():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})

        return render_template('information.html', id=user_info["id"], name=user_info["name"], age=user_info["age"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


# 정보변경 API

@app.route('/api/information', methods=['post'])
def api_information():
    token_receive = request.cookies.get('mytoken')
    idload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": idload['id']})

    id_receive = user_info["id"]
    current_password = user_info['pw']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    if current_password == pw_hash:
        print(pw_hash, current_password)
        return jsonify({'result': 'fail', 'msg': '동일한 비밀번호는 사용할 수 없습니다'})
    else:
        result = db.users.find_one({'id': id_receive, 'pw': current_password})
        print("다른 비밀 번호", result)
        if result is not None:
            db.users.update_one({'id': id_receive}, {
                                '$set': {'pw': pw_hash}, })
        return jsonify({'result': 'success', 'msg': '정보변경 완료!'})
    

# 로그인
@app.route('/api/profile')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 로그인시 토큰발급 API
@app.route('/api/profile/login', methods=['POST'])
def sign_in():
    # 입력받은 아이디 비밀번호 변수에 저장
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 비밀번호 해쉬화 후 pw_hash 변수에 저장
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 아이디와 해쉬화된 비밀번호가 데이터베이스의 내용과 같은지 확인
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash})

    # 아이디 비밀번호가 일치하는 경우
    if result is not None:
        # 유저의 아이디와 24시간유지되는 유효시간을 payload에 저장
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # 저장된 payload를 jwt 토큰으로 인코드
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # 토큰값 리턴
        return jsonify({'result': 'success', 'token': token})
    # 아이디 비밀번호가 일치하지 않는경우
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



# 회원가입 API
@app.route('/api/profile/regist', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    name_receive = request.form['name_give']
    gender_receive = request.form['gender_give']
    age_receive = request.form['age_give']
    password_hash = hashlib.sha256(
        password_receive.encode('utf-8')).hexdigest()

    doc = {
        "id": username_receive,                                # 아이디
        "pw": password_hash,                                   # 비밀번호
        "name": name_receive,                                  # 이름
        "age": age_receive,                                    # 나이
        "gender": gender_receive,                              # 성별
        "like": "",                                            # 좋아요
        "favorite": ""                                         # 즐겨찾기
    }
    # 입력받은 회원정보 데이터베이스에 저장
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 아이디 중복체크
@app.route('/api/profile/regist/check_dup', methods=['POST'])
def check_dup():
    # 아이디 입력받음
    username_receive = request.form['username_give']
    # 입력받은 아이디와 동일한 아이디 존재여부 확인 (true/false)
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 데이터베이스에서 비디오 불러오기
@app.route("/api/videos", methods=["GET"])
def videos_get():
    list_videos = list(db.videos.find({}, {'_id': False}))
    return jsonify({'list': list_videos})


# 불러온 비디오 부위별로 불러오기
@app.route("/api/videos/buName", methods=["POST"])
def videos_post():
    bu_name = request.form['buName_give']
    list_videos = list(db.videos.find({'bu_name': bu_name}, {'_id': False}))
    return jsonify({'list': list_videos})


# 댓글 저장 API
@app.route('/api/post_comment', methods=['POST'])
def post_comment():
    # 댓글 쓰기
    id_receive = request.form['id_give']
    comment_receive = request.form['comment_give']
    comment_id_receive = request.form['comment_id_give']
    user_receive = request.form['user_give']
    video_id_receive = request.form['video_id_give']

    doc = {
        'id': id_receive,
        'name': user_receive,
        'comment': comment_receive,
        'comment_id': comment_id_receive,
        'video_id': video_id_receive,
    }

    db.comments.insert_one(doc)
    try:
        commentarr_temp = db.videos.find_one(
            {'video_id': video_id_receive})['comment_id']
    except:
        doc = {'comment_id': ['지워지면 안됨니다', '***************']}
        db.videos.update_one({'video_id': video_id_receive}, {'$set': doc})
    commentarr_temp = db.videos.find_one(
        {'video_id': video_id_receive})['comment_id']
    cm = []

    for comment in commentarr_temp:
        cm.append(comment)
    cm.append(comment_id_receive)
    db.videos.update_one({'video_id': video_id_receive},
                         {'$set': {'comment_id': cm}})

    return jsonify({'result': 'success', 'msg': '댓글이 저장되었습니다!'})


# 댓글 삭제 API
@app.route('/api/delete_comment', methods=['POST'])
def delete_comment():
    comment_id_receive = request.form['comment_id_give']
    video_id_receive = request.form['video_id_give']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload['id']})['id']

    writer = db.comments.find_one({'comment_id': comment_id_receive})['id']

    if user_info == writer:
        commentarr_temp = db.videos.find_one(
            {'video_id': video_id_receive})['comment_id']
        cm = []
        for comment in commentarr_temp:
            cm.append(comment)
        cm.remove(comment_id_receive)
        db.videos.update_one({'video_id': video_id_receive}, {
                             '$set': {'comment_id': cm}})
        db.comments.delete_one({'comment_id': comment_id_receive})

        return jsonify({'result': 'success', 'msg': '댓글이 삭제되었습니다🙆'})
    else:
        return jsonify({'result': 'fail', 'msg': '다른 유저의 댓글을 삭제할 수 없습니다🙅‍♀️'})


# 댓글 불러오기
@app.route('/api/get_comment', methods=['GET'])
def get_comment():
    video_id_receive = request.args.get('video_id_give')
    result = list(db.comments.find({'video_id': video_id_receive}))
    arr = []
    if result is not None:
        for re in result:
            temp = {
                'comment': re['comment'],
                'comment_id': re['comment_id'],
                'id': re['id'],
                'video_id': re['video_id'],
                'name': re['name']
            }
            arr.append(temp)
    return jsonify({'result': 'success', 'comment': arr})


# 좋아요 갯수 불러오기
@app.route('/api/get_like', methods=['GET'])
def get_like():
    video_id_receive = request.args.get('video_id_give')
    user_id_receive = request.args.get('user_id_give')

    userliked = db.users.find_one({'id': user_id_receive})['like']

    if video_id_receive in userliked:
        liked = True
    else:
        liked = False

    try:
        count = db.videos.find_one({'video_id': video_id_receive})[
            'like_count']
    except:
        doc = {'like_count': 0}
        db.videos.update_one({'video_id': video_id_receive}, {'$set': doc})
        count = db.videos.find_one({'video_id': video_id_receive})[
            'like_count']

    return jsonify({'result': 'success', 'count': count, 'isliked': liked})


# 좋아요 추가
@app.route('/api/add_like', methods=['POST'])
def add_like():
    id_receive = request.form['id_give']
    video_id_receive = request.form['video_id_give']

    count = db.videos.find_one({'video_id': video_id_receive})['like_count']

    like = list(db.users.find_one({'id': id_receive})['like'])

    if video_id_receive not in like:
        like.append(video_id_receive)
        count = count + 1
        db.videos.update_one({'video_id': video_id_receive}, {
                             '$set': {'like_count': count}})
        db.users.update_one({'id': id_receive}, {'$set': {'like': like}})

    return jsonify({'result': 'success', 'count': count})


# 좋아요 해제
@app.route('/api/undo_like', methods=['POST'])
def undo_like():
    id_receive = request.form['id_give']
    video_id_receive = request.form['video_id_give']

    count = db.videos.find_one({'video_id': video_id_receive})['like_count']
    like = list(db.users.find_one({'id': id_receive})['like'])

    if video_id_receive in like:
        like.remove(video_id_receive)
        count = count - 1
        db.videos.update_one({'video_id': video_id_receive}, {
                             '$set': {'like_count': count}})
        db.users.update_one({'id': id_receive}, {'$set': {'like': like}})

    return jsonify({'result': 'success', 'count': count})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
