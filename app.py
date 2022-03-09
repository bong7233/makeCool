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


@app.route('/')
def home():
    return render_template('login.html')


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
    # pymongo에 pw변경
    return jsonify({'result': 'success', 'msg': '정보변경 완료!'})


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
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/api/profile/regist/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 여기 있었던 main/부위는 전부 삭제 해주세요
# @app.route("/api/main/neck", methods=["GET"])
# def necklist_get():
#     list_neck = list(db.neck.find({}, {'_id': False}))
#     return jsonify({'main_list': list_neck})

################### 김지호 수정 #####################################################
@app.route("/api/videos", methods=["GET"])
def videos_get():
    list_videos = list(db.videos.find({}, {'_id': False}))
    return jsonify({'list': list_videos})


@app.route("/api/videos/buName", methods=["POST"])
def videos_post():
    bu_name = request.form['buName_give']
    list_videos = list(db.videos.find({'bu_name': bu_name}, {'_id': False}))
    return jsonify({'list': list_videos})


################### 김지호 수정 ###################################################


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


@app.route('/api/delete_comment', methods=['POST'])
def delete_comment():
    # 댓글 쓰기
    comment_id_receive = request.form['comment_id_give']
    video_id_receive = request.form['video_id_give']
    user_name_receive = request.form['user_name_give']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload['id']})['id']

    writer = db.comments.find_one({'comment_id': comment_id_receive})['id']

    if user_info == writer:
        # array = db.video.find_one({'video_id' : video_id_receive})['comment_id']
        # print(array)
        # deltedarray = array.remove(comment_id_receive)

        commentarr_temp = db.videos.find_one(
            {'video_id': video_id_receive})['comment_id']
        cm = []
        for comment in commentarr_temp:
            cm.append(comment)
        cm.remove(comment_id_receive)
        db.videos.update_one({'video_id': video_id_receive}, {
                             '$set': {'comment_id': cm}})

        # db.video.update_one({"video_id": video_id_receive},{'$set' : {'comment_id' : deltedarray}})
        db.comments.delete_one({'comment_id': comment_id_receive})

        return jsonify({'result': 'success', 'msg': '댓글이 삭제되었습니다🙆'})
    else:
        return jsonify({'result': 'fail', 'msg': '다른 유저의 댓글을 삭제할 수 없습니다🙅‍♀️'})


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
    print(arr)
    return jsonify({'result': 'success', 'comment': arr})


@app.route('/api/get_like', methods=['GET'])
def get_like():
    video_id_receive = request.args.get('video_id_give')
    user_id_receive = request.args.get('user_id_give')

    print('user id is : ' + user_id_receive)

    userliked = db.users.find_one({'id': user_id_receive})['like']
    print(userliked)

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

    print(count)
    return jsonify({'result': 'success', 'count': count, 'isliked': liked})


@app.route('/api/add_like', methods=['POST'])
def add_like():
    # 좋아요 추가
    id_receive = request.form['id_give']
    video_id_receive = request.form['video_id_give']

    count = db.videos.find_one({'video_id': video_id_receive})['like_count']

    like = list(db.users.find_one({'id': id_receive})['like'])

    if video_id_receive not in like:
        like.append(video_id_receive)
        print(like)
        count = count + 1
        db.videos.update_one({'video_id': video_id_receive}, {
                             '$set': {'like_count': count}})
        db.users.update_one({'id': id_receive}, {'$set': {'like': like}})

    return jsonify({'result': 'success', 'count': count})


@app.route("/api/videos/favorite", methods=["POST"])
def favorite_post():
    token_receive = request.cookies.get('mytoken')

    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload['id']})
    doc = {
        'name': user_info['name'],
        'id': user_info['id'],
        'like': user_info['like'],
        'favorite': user_info['favorite']
    }
    bu_name = request.form['buName_give']
    list_videos = list(db.videos.find({'bu_name': bu_name}, {'_id': False}))
    return jsonify({'list': list_videos})


# # # # # # # # # 여기여기여기


@app.route("/api/videos/favorite", methods=["GET"])
def videos_p():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = (db.users.find_one({"id": payload['id']})['like'])
        print(user_info)

        # posts = list(db.posts.find({}).sort("date", -1).limit(20))
        # #                     다들고와서      작성된순차 최근. 리밋20개
        # print(posts)
        # for post in posts:
        #     post["_id"] = str(post["_id"])
        # #     _id값을 _id값은 오브젝트여서 str값으로 변환 문자열로 변환
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", 'favorites': user_info})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
    # list_videos = list(db.videos.find({}, {'_id': False}))
    #


@app.route('/api/undo_like', methods=['POST'])
def undo_like():
    # 좋아요 해제
    id_receive = request.form['id_give']
    video_id_receive = request.form['video_id_give']

    count = db.videos.find_one({'video_id': video_id_receive})['like_count']
    like = list(db.users.find_one({'id': id_receive})['like'])

    if video_id_receive in like:
        like.remove(video_id_receive)
        msg = "좋아요 해지"
        count = count - 1
        db.videos.update_one({'video_id': video_id_receive}, {
                             '$set': {'like_count': count}})
        db.users.update_one({'id': id_receive}, {'$set': {'like': like}})

    else:
        msg = '좋아요 하지 않은 개시글 입니다'

    return jsonify({'result': 'success', 'count': count})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
