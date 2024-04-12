# 마스터 db 테이블 정의

def m_tbs(cursor):
    # 유저 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_idx INTEGER PRIMARY KEY,                      
                      user_id VARCHAR NOT NULL UNIQUE,
                      user_pw VARCHAR NOT NULL,
                      user_name VARCHAR NOT NULL,
                      created_date DATE NOT NULL
                      )                      
    ''')
    # 유저 테이블과 회사 테이블의 중간 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS userToCom
                      (user_idx INTEGER UNIQUE,
                       com_idx INTEGER UNIQUE,                 
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx),                                   
                      FOREIGN KEY (com_idx) REFERENCES com_list(com_idx)
                     )                    
    ''')

    # 토큰 인증 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS token
                     (token_idx INTEGER PRIMARY KEY,
                      payload VARCHAR NOT NULL UNIQUE,
                      user_idx INTEGER UNIQUE,
                      status VARCHAR,
                      exp_date DATE,
                      created_date DATE,                      
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx)                                   
                     )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_imgs
                     (img_idx INTEGER PRIMARY KEY,
                      user_idx INTEGER NOT NULL,
                      o_img_name VARCHAR NOT NULL,
                      s_img_name VARCHAR NOT NULL,
                      img_size INTEGER NOT NULL,
                      img_type VARCHAR NOT NULL,
                      img_ext VARCHAR(10) NOT NULL,
                      img_path VARCHAR NOT NULL,
                      domain VARCHAR NOT NULL,
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx)
                     )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                     (info_idx INTEGER PRIMARY KEY,
                      user_idx INTEGER NOT NULL,
                      c_name VARCHAR NOT NULL,
                      c_value VARCHAR NOT NULL,
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx)                   
                     )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS com_list
                     (com_idx INTEGER PRIMARY KEY,                      
                      owner_name VARCHAR NOT NULL,
                      c_name VARCHAR NOT NULL,
                      c_id VARCHAR NOT NULL UNIQUE,
                      chan_yn VARCHAR(1) NOT NULL,   
                      created_date date NOT NULL                  
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS file_user
                     (idx INTEGER PRIMARY KEY,
                      com_idx INTEGER NOT NULL,
                      f_idx INTEGER NOT NULL,
                      FOREIGN KEY (f_idx) REFERENCES file_upload(f_idx),
                      FOREIGN KEY (com_idx) REFERENCES com_list(com_idx)                                                      
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_upload
                     (f_idx INTEGER PRIMARY KEY,
                      o_f_name VARCHAR NOT NULL,
                      s_f_name VARCHAR NOT NULL,
                      f_size INTEGER NOT NULL,
                      f_type VARCHAR NOT NULL,
                      f_ext VARCHAR NOT NULL,
                      f_path VARCHAR NOT NULL,
                      domain VARCHAR NOT NULL                                                      
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS com_info
                     (info_idx INTEGER PRIMARY KEY,
                      com_idx INTEGER,
                      c_name VARCHAR,
                      c_value VARCHAR,
                      FOREIGN KEY (com_idx) REFERENCES com_list(com_idx)                                                      
                      )''')