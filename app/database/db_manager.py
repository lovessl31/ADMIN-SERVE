# 디비 생성 및 관리 담당파일
import os
import sqlite3
from werkzeug.security import generate_password_hash
from app.database.models.m_t_db import m_tbs
from app.database.models import customer, company, category, board, fileUpload, option
from datetime import datetime


'''
1. main db 생성하기
2. sub db 생성하기
'''

# DB 폴더 경로
MAIN_DB_PATH1 = "C:\withchat_db\main"
# DB 파일 경로
MAIN_DB_PATH2 = os.path.join(MAIN_DB_PATH1, "main.db")
def create_main_db():
    os.makedirs(MAIN_DB_PATH1, exist_ok=True)
    # 디비생성 ,연결
    conn = sqlite3.connect(MAIN_DB_PATH2)
    cursor = conn.cursor()

    # 테이블 등록
    m_tbs(cursor)
    # 커밋 및 연결 종료
    conn.commit()
    conn.close()

SUB_DB_PATH1 = "C:\withchat_db\sub"
def create_company_db(company_name):
    SUB_DB_PATH2 = os.path.join(SUB_DB_PATH1, f"{company_name}.db")
    os.makedirs(SUB_DB_PATH1, exist_ok=True)

    # 생성과연결
    conn = sqlite3.connect(SUB_DB_PATH2)
    cursor = conn.cursor()

    # 테이블 등록
    customer.c_user_tbs(cursor)
    board.c_board_tbs(cursor)
    category.c_cate_tbs(cursor)
    company.c_com_tbs(cursor)
    fileUpload.c_file_tbs(cursor)
    option.c_option_tbs(cursor)
    conn.commit()
    conn.close()


def insert_user():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pw = generate_password_hash('1')
    conn = sqlite3.connect(MAIN_DB_PATH2)
    cursor = conn.cursor()
    user_id = 'admin'
    cursor.execute('''SELECT user_id FROM users WHERE user_id = ?''', (user_id,))
    check_id = cursor.fetchone()
    if check_id:
        return
    else:
        cursor.execute('''INSERT INTO users(user_id, user_pw, user_name, created_date)
        VALUES(?,?,?,?)
        ''', (user_id , pw, '관리자', current_datetime))

        cursor.execute('''INSERT INTO com_list(owner_name, c_name, c_id, chan_yn, created_date)
                VALUES(?,?,?,?,?)
                ''', ("with", "first", "777", "Y", current_datetime))
        cursor.execute('''INSERT INTO userToCom(user_idx, com_idx)
                VALUES(?,?)
                ''', (1, 1))
        create_company_db("777")
    conn.commit()
    conn.close()



create_main_db()
insert_user()

