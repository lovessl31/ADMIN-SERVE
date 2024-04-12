def c_user_tbs(cursor):
    # 유저 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_idx INTEGER PRIMARY KEY,
                      user_id VARCHAR NOT NULL UNIQUE,
                      user_pw VARCHAR NOT NULL,
                      user_name VARCHAR NOT NULL,
                      status VARCHAR(1) NOT NULL,
                      created_date DATE NOT NULL                       
                      )''')
    # 유저 테이블과 회사 테이블의 중간 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS userToCom
                      (user_idx INTEGER UNIQUE,
                       com_idx INTEGER UNIQUE,                 
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx),                                   
                      FOREIGN KEY (com_idx) REFERENCES com_list(com_idx)
                     )                    
    ''')
    # 유저 참조 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                     (info_idx INTEGER PRIMARY KEY,
                      user_idx INTEGER NOT NULL UNIQUE,
                      c_name VARCHAR,
                      c_value VARCHAR,      
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx)          
                     )''')

    # 유저 권한 그룹 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS User_RoleGroup
                     (idx INTEGER PRIMARY KEY,
                      user_idx INTEGER,
                      role_id VARCHAR NOT NULL UNIQUE,
                      FOREIGN KEY (user_idx) REFERENCES users(user_idx)                                    
                     )''')
    # 유저 권한 설정 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS Role
                     (idx INTEGER PRIMARY KEY,
                      role_id VARCHAR NOT NULL UNIQUE,
                      role_name VARCHAR NOT NULL,
                      FOREIGN KEY (role_id) REFERENCES User_RoleGroup(role_id)                                   
                     )''')

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
    
    # 유저 프로필 테이블
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











