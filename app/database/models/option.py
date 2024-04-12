def c_option_tbs(cursor):
    # 옵션 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS option_table
                        (o_idx INTEGER PRIMARY KEY NOT NULL,
                         o_value VARCHAR ,
                         o_name VARCHAR ,
                         o_group VARCHAR ,
                         sort_order INTEGER,
                         created_date DATE,
                         update_date DATE
                         )
                      ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS option_user
                        (idx INTEGER PRIMARY KEY,
                         user_idx INTEGER NOT NULL,
                         o_value VARCHAR NOT NULL,
                         FOREIGN KEY (o_value) REFERENCES option_table(o_value),
                         FOREIGN KEY (user_idx) REFERENCES users(user_idx)
                         )
                      ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS option_post
                        (idx INTEGER PRIMARY KEY,
                         post_idx INTEGER NOT NULL,
                         o_value VARCHAR NOT NULL,
                         FOREIGN KEY (o_value) REFERENCES option_table(o_value),
                         FOREIGN KEY (post_idx) REFERENCES post(post_idx)
                         )
                      ''')