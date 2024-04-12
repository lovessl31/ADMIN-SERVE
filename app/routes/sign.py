from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token,jwt_required, create_refresh_token, get_jwt, decode_token,get_jwt_identity
from flask import request, jsonify
import sqlite3
from app.database import db_manager as DB
from app.utils import upload_parser, file_upload
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app import app, jwt_blocklist


sign_api = Namespace('Sign', description='사용자 등록 API', path='/with')


# 로그인 실패 카운팅 변수
login_fails = {}
login_fails_limit = 5

# 로그인
@sign_api.route('/login')
@sign_api.doc(description="로그인", params={'user_id':'사용자 이메일','user_pw': '사용자 비밀번호'},
              responses={200: '로그인 성공'})
class login(Resource):
    """
      사용자 정보 엔드포인트

      이 엔드포인트는 사용자 정보를 처리합니다.
      """

    def post(self):
        """
        로그인

        POST 요청으로 사용자의 login을 처리합니다.
        """

        data = request.json
        user_id = data['user_id']
        user_pw = data['user_pw']

        if data:

            # 유저 아이디 조회
            with sqlite3.connect(DB.MAIN_DB_PATH2) as conn:
                cursor = conn.cursor()

                cursor.execute('''SELECT user_id, user_pw, user_idx FROM users
                                WHERE user_id = ?''', (user_id,))
                user = cursor.fetchone()
                cursor.execute('''SELECT com_idx FROM userToCom 
                                                WHERE user_idx = ?''', (user[2],))
                com_idx = cursor.fetchone()[0]
                print("login com_idx in :::::", com_idx)
                if user:
                    if check_password_hash(user[1], user_pw):
                        #로그인 성공시 로그인 횟수 초기화
                        login_fails.pop(user_id, None)
                        
                        user_info = {"user_id": user[0],
                                     "user_idx": user[2],
                                     "role": "5"}
                        # 회사가 존재하면 회사정보 삽입
                        if com_idx is not None:
                            user_info["com_idx"] = com_idx
                        # 토큰 발급
                        access_token = create_access_token(identity=user_info)
                        refresh_token = create_refresh_token(identity=user_info)
                        print("리프레시 토큰:" + refresh_token)
                        print("엑세스토큰:" + access_token)

                        try:
                            r_token_data = decode_token(refresh_token)
                            created_at = datetime.fromtimestamp(r_token_data.get('iat'))  # 토큰 생성일
                            expired_at = datetime.fromtimestamp(r_token_data.get('exp'))  # 토큰 만료일
                            status = 'N'  # 토큰 취소 여부
                            print(created_at, expired_at)

                            conn = sqlite3.connect(DB.MAIN_DB_PATH2)
                            cursor = conn.cursor()

                            # 존재하는 토큰인지 확인하여 업데이트 또는 새로운 토큰 추가
                            cursor.execute("SELECT user_idx, user_name FROM users WHERE user_id = ?", (user_id,))
                            row = cursor.fetchone()
                            user_idx = row[0]  # 첫 번째 컬럼인 user_idx
                            user_name = row[1]  # 두 번째 컬럼인 user_name

                            cursor.execute("SELECT * FROM token WHERE user_idx = ?", (user_idx,))
                            existing_token = cursor.fetchone()
                            if existing_token:
                                # 토큰 업데이트
                                cursor.execute(
                                    "UPDATE token SET payload=?, created_date=?, exp_date=?, status=? WHERE user_idx = ?",
                                    (refresh_token, created_at, expired_at, status, user_idx))
                            else:
                                # 새로운 토큰 추가
                                cursor.execute(
                                    "INSERT INTO token (payload, user_idx, created_date, exp_date, status) VALUES (?, ?, ?, ?, ?)",
                                    (refresh_token, user_idx, created_at, expired_at, status))
                            conn.commit()
                            conn.close()
                        except KeyError:
                            conn.close()
                            print("토큰에 필수 필드가 없습니다.")
                        return jsonify({
                                        'loginMsg': "Y",
                                        "accessToken": access_token,
                                        "refreshToken": refresh_token,
                                        "resultCode": 200,
                                        'resultDesc': "Success",
                                        'resultMsg': f'{user_name}님 환영합니다.'
                                        },200)

                    else:
                        login_fails[user_id] = login_fails.get(user_id, 0) + 1
                        if login_fails[user_id] >= login_fails_limit:
                            return {"error": 'Login attempts exceeded limit'}, 400

                        return {'loginMsg': "N",
                                'accessToken': "",
                                'refreshToken': "",
                                'resultCode': 401,
                                'resultDesc': "Unauthorized",
                                'resultMsg': "비밀번호를 다시 확인해주세요."}, 401
                else:
                    return {"error": '해당하는 사용자가 존재하지 않습니다.'}, 400
        else:
            return {"error": "요청에 데이터가 포함되어 있지 않습니다."}, 400






# 액세스 토큰 재발급 엔드포인트
@sign_api.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        data = get_jwt_identity()
        print(data)
        print(f"데이타:{data}")
        refresh_token = request.headers['Authorization'].replace('Bearer ', '')
        print(f"리프레시토큰:{refresh_token}")
        if refresh_token:
            refresh_token_data = decode_token(refresh_token)
            print(refresh_token_data)
            try:
                conn = sqlite3.connect(DB.MAIN_DB_PATH2)
                cursor = conn.cursor()
                cursor.execute('''SELECT payload FROM token WHERE payload = ?''', (refresh_token,))
                is_rf_token = cursor.fetchone()[0]
                conn.commit()
                conn.close()
                user_info = {"user_id": data['user_id'],
                             "user_idx": data['user_idx'],
                             "role": data['role']}
                if data['com_idx'] is not None:
                    user_info["com_idx"] = data['com_idx']

                if is_rf_token == refresh_token:
                    access_token = create_access_token(identity=user_info)
                    return jsonify({"accessToken":access_token,
                                          "resultCode": 200,
                                          'resultDesc': "Success"}, 200)
                else:
                    return jsonify({"error": '일치하는 토큰이 없습니다.'}, 400)
            except sqlite3.Error as e:
                return "SQLite error: " + str(e)
            finally:
                conn.close()
        else:
            return jsonify({"error": "요청에 토큰 데이터가 포함되어 있지 않습니다."}, 400)



@sign_api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  # jti : 토큰을 고유ID로 저장
        rrr = get_jwt()
        print(rrr)
        jwt_blocklist.add(jti)  # jwt_blocklist : 토큰의 고유ID, 토큰 유지 기간, 토큰 유지 기간 설정 여부
        response = jsonify(msg='로그아웃이 정상처리되었습니다.')
        # 쿠키에서 토큰 삭제
        response.set_cookie(app.config['JWT_ACCESS_COOKIE_NAME'], '', expires=0)
        response.set_cookie(app.config['JWT_REFRESH_COOKIE_NAME'], '', expires=0)
        return response  # jwt_bloacklist에 jti만 넣어주고 나머지 생략하면 토큰 즉시 파괴


@sign_api.route('/signup')
@sign_api.doc(description="회원 등록",
              params={'user_id':'사용자 이메일',
                      'user_pw': '사용자 비밀번호',
                      'user_name':'사용자 명',
                      'status':'등록 상태' ,
                      'role_id' :'유저 유형(integer)',
                      'role_name': '규칙 명'},
              responses={200: '로그인 성공'})
class signup(Resource):
    def post(self):
        """
                회원가입

                POST 요청으로 사용자의 회원가입을 처리합니다.
                """

        data = request.json

        if data:
            if data['user_id'] & data['user_pw'] & data['user_name'] & data['role_id'] & data['role_name']:
               user_id = data['user_id']
               # 받아온 비밀번호 바로 해싱
               user_pw = generate_password_hash(data['user_pw'])
               print(user_id, user_pw)


        else : return {"error": "요청에 데이터가 포함되어 있지 않습니다."}, 400


@sign_api.route('/com-info')
class comInfo(Resource):
    @sign_api.expect(upload_parser)
    @sign_api.doc(description="회사등록", params={'owner_name':'대표자명','c_id': '사업자등록번호', 'c_name': '회사명'}, responses={200: '회사등록성공'})
    def post(self):
        """
                회사등록

                POST 요청으로 사용자의 회사정보 등록을 처리합니다.
                """
        # form 형식의 데이터 받아오기
        data = request.form
        f_data = upload_parser.parse_args()
        # 받아온 데이터 확인 및 처리
        if f_data and data is not None:
            owner_name = data.get('owner_name')
            com_name = data.get('c_name')
            com_id = data.get('c_id')
            chan = 'Y' # 일단은 Y 처리하고 추후에 기능생기면 로직추가하기로.
            created_date = datetime.now()

            # 회사 정보를 마스터 DB에 저장
            conn = sqlite3.connect(DB.MAIN_DB_PATH2)
            cursor = conn.cursor()

            try:
                cursor.execute('''
                                    INSERT INTO com_list (owner_name, c_name, c_id, chan_yn, created_date)
                                    VALUES (?, ?, ?,?,?)
                                    ''', (owner_name, com_name, com_id, chan, created_date))
                com_idx = cursor.lastrowid
                conn.commit()
                conn.close()
                file_upload("file1","C:\withchat_db", "http://withfirst.com/fileupload", com_idx)
                # 회사 DB 생성
                if chan == 'Y':
                    DB.create_company_db(com_id)
                return jsonify({"Add Company": "Company registration has been successfully completed"})

            except sqlite3.Error as e:
                return {"error":str(e)}, 500

            finally:
                conn.close()

        else: return {"error": "요청에 데이터가 포함되어 있지 않습니다."}, 400

    def get(self):
        conn = sqlite3.connect(DB.MAIN_DB_PATH2)
        cursor = conn.cursor()
        cursor.execute('''
            select c_name from com_list
        ''')
        result = cursor.fetchall()
        conn.close()
        return jsonify({"회사목록": result})



