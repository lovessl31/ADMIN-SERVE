import sqlite3
from flask_restx import reqparse
from werkzeug.utils import secure_filename
import app.database.db_manager as DB
from datetime import datetime
import time



# 파일 유효성 검사를 위한 함수
# 파일 업로드
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar'}
ALLOWED_EXTENSIONS |= {ext.upper() for ext in sorted(ALLOWED_EXTENSIONS)}
# 이미지 파일
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}

def valid_file(value, field_name):
    # 'file' 필드에 대한 유효성 검사
    if field_name == 'file':
        allowed_extensions = ALLOWED_EXTENSIONS
    # 'img' 필드에 대한 유효성 검사
    elif field_name == 'img':
        allowed_extensions = ALLOWED_EXTENSIONS_IMG
    else:
        raise ValueError("유효하지 않은 필드 이름입니다.")

    # 파일 확장자를 확인하고 유효한지 검사합니다.
    if '.' not in value.filename or value.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        raise ValueError('유효하지 않은 파일 형식입니다.')

    return value


# 파일 업로드를 위한 RequestParser 생성
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=lambda x: valid_file(x, 'file'), required=True,
                           help='파일')
upload_parser.add_argument('file', location='files', type=lambda x: valid_file(x, 'img'), required=True,
                           help='이미지 파일')



# 파일 업로드 함수
def file_upload(save_f_name, f_path, domain, com_idx , db_path=DB.MAIN_DB_PATH2):
    f_data = upload_parser.parse_args()
    f = valid_file(f_data['file'], field_name='file')
    o_f_name = f.filename  # 원본 파일명
    f_type = f.content_type  # 파일유형
    ext = o_f_name.split('.')[-1].lower()  # 확장자
    filename = secure_filename(o_f_name)
    mkdir_p(f_path)
    # 파일 저장
    f.save(os.path.join(f_path, filename))
    # 저장된 파일의 용량을 가져오기
    f_size = convert_size(os.path.getsize(f"{f_path}\{filename}"))
    print(o_f_name, save_f_name, f_size, f_type, ext, f_path, domain)
    # 별다른 값이 없으면 메인 db 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
                        INSERT INTO file_upload (o_f_name, s_f_name, f_size, f_type, f_ext, f_path, domain)
                        VALUES (?,?,?,?,?,?,?)
                        ''', (o_f_name, save_f_name, f_size, f_type, ext, f_path, domain))
    f_idx = cursor.lastrowid
    cursor.execute('''
                        INSERT INTO file_user (com_idx, f_idx)
                        VALUES (?,?)
                        ''', (com_idx, f_idx))
    conn.commit()
    conn.close()

# 유저 프로필 함수
def img_upload(s_img_name, img_path, domain, user_idx , db_path=DB.MAIN_DB_PATH2):
    f_data = upload_parser.parse_args()
    f = valid_file(f_data['file'], field_name='img')
    o_img_name = f.filename  # 원본 이미지 파일명
    img_type = f.content_type  # 이미지 파일 유형
    ext = o_img_name.split('.')[-1].lower()  # 확장자
    filename = secure_filename(o_img_name)
    mkdir_p(img_path)
    f.save(os.path.join(img_path, filename))
    img_size = convert_size(os.path.getsize(f"{img_path}\{filename}"))
    print(o_img_name, s_img_name, img_size, img_type, ext, img_path, domain)
    # 별다른 값이 없으면 메인 db 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
                        INSERT INTO user_imgs (user_idx,o_img_name, s_img_name, img_size, img_type, img_ext, img_path, domain)
                        VALUES (?,?,?,?,?,?,?)
                        ''', (user_idx, o_img_name, s_img_name, img_size, img_type, ext, img_path, domain))
    conn.commit()
    conn.close()

# 파일 사이즈 구하는 함수
def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])




import os
import errno
#  파이썬 옛버전이라 ok기능을 사용못해서 만든 함수.
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path): #파일이 존재하면서 그게 디렉토리인 경우
            pass
        else:
            raise


# 토큰정보로 회사db 경로 가져오기
def get_t_com(token):
    print("token :",token)
    if token and "com_idx" in token:
        user_idx = token["user_idx"]
        com_idx = token["com_idx"]
        role = token["role"]

        # 만약 role이 관리자라면 모든 회사의 db 경로를 줘야함.

        # 유저정보를 토대로 검색
        conn = sqlite3.connect(DB.MAIN_DB_PATH2)
        cursor = conn.cursor()

        cursor.execute('''SELECT c_id
                          FROM com_list
                          WHERE com_idx = ?
        ''', (com_idx,))
        c_id = cursor.fetchone()[0]
        # 접속 DB 경로 설정
        path = f"{DB.SUB_DB_PATH1}\{c_id}.db"
        print(get_db_files(DB.SUB_DB_PATH1))
        # 서브디비경로, 유저idx, 회사idx를 보내주기
        if role == '5': # 관리자라면
            return [get_db_files(DB.SUB_DB_PATH1), user_idx, com_idx]
        # 관리자가 아니라면
        else: return [path, user_idx, com_idx]
    else:
        return False


# 경로에 있는 모든 DB 리스트에 담기
def get_db_files(path):
    db_files = []
    for file in os.listdir(path):
        if file.endswith('.db'):
            db_files.append(os.path.join(path, file))
    return db_files

# 서브 DB 폴더 경로에 있는 모든 db파일을 변수에 저장
db_files = get_db_files(DB.SUB_DB_PATH1)
# 메인 DB 파일도 변수에 추가
db_files.append(DB.MAIN_DB_PATH2)




from concurrent.futures import ThreadPoolExecutor

def connect_to_db(db_path, keyword):
    if isinstance(db_path, str):  # 문자열인 경우에만 연결 설정
        if keyword == 'category': # 카테고리 전체조회
            categories = []
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM category''')
            for row in cursor.fetchall():
                cate_val = list(row)
                cursor.execute('''SELECT tag_name FROM c_tag WHERE cate_idx = ?''', (cate_val[0],))
                tag = cursor.fetchall()
                # null 값 0으로
                if cate_val[1] is None:
                    cate_val[1] = 0
                categories.append({'cateNo': cate_val[0],
                                   'subCateNo': cate_val[1],
                                   'categoryName': cate_val[2],
                                   'categoryType': cate_val[3],
                                   'role': cate_val[4],
                                   'visibility': cate_val[5],
                                   'likeSet': cate_val[6],
                                   'tag': tag
                                   })
            conn.commit()
            conn.close()
        else: return None



def connect_to_dbs(path_list, keyword):
    results = {}
    with ThreadPoolExecutor() as executor:
        for path in path_list:
            # 여러 키워드에 대한 쿼리 수행
            results[path] = {}
            results[path][f"{keyword}"] = connect_to_db(path, keyword)
            print(results)
    return results


# 타입판별
def is_list(v):
    if isinstance(v, list):
        return True
    else:
        return False





# 토큰 삭제 함수
import threading

def delete_expired_tokens(path):
    retries = 3
    while retries > 0:
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            current_time = datetime.now()
            print(current_time)
            cursor.execute('DELETE FROM token WHERE exp_date < ?', (current_time,))
            conn.commit()
            break  # 해당 경로의 토큰 삭제가 성공하면 루프 탈출
        except sqlite3.OperationalError as e:
            print("데이터베이스 잠금 발생:", e)
            retries -= 1
            time.sleep(1)  # 일정 시간 동안 대기한 후 다시 시도합니다.
        finally:
            conn.close()
    else:
        print("데이터베이스에 잠금이 지속되어 작업을 수행할 수 없습니다.")

# 병렬로 토큰 삭제 수행하는 함수
def parallel_delete_expired_tokens(paths):
    threads = []  # 스레드를 담을 리스트 생성
    for path in paths:  # 모든 경로에 대해 반복
        # 각 경로를 처리하는 스레드 생성
        thread = threading.Thread(target=delete_expired_tokens, args=(path,))
        thread.start()  # 스레드 시작
        threads.append(thread)  # 생성된 스레드를 리스트에 추가

    for thread in threads:
        thread.join()  # 모든 스레드가 종료될 때까지 대기

    time.sleep(3600)  # 1시간마다 실행을 위해 대기

# 백그라운드 스레드 생성 및 실행
token_cleanup_thread = threading.Thread(target=parallel_delete_expired_tokens, args=(db_files,))
token_cleanup_thread.daemon = True  # 메인 스레드 종료 시 자동 종료
token_cleanup_thread.start()  # 스레드 시작








