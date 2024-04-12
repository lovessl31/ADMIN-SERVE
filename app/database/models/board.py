def c_board_tbs(cursor):
    # 게시판
    cursor.execute('''CREATE TABLE IF NOT EXISTS board
                          (board_idx INTEGER PRIMARY KEY NOT NULL,
                           cate_idx INTEGER NOT NULL,
                           board_name VARCHAR NOT NULL,
                           board_desc VARCHAR,
                           created_date DATE NOT NULL,
                           FOREIGN KEY (cate_idx) REFERENCES CategoryToBoard(cate_idx)                                                                                                                                    
                          )''')
    # 게시글
    cursor.execute('''CREATE TABLE IF NOT EXISTS post
                          (post_idx INTEGER PRIMARY KEY NOT NULL,
                          board_idx INTEGER NOT NULL,
                          cate_idx INTEGER NOT NULL,
                          p_view INTEGER NOT NULL,
                          p_seq VARCHAR(50),
                          user_idx INTEGER,
                          user_name VARCHAR(50),
                          p_title VARCHAR(100),
                          p_content VARCHAR,
                          update_date DATE NOT NULL,
                          del_yn VARCHAR(1),                                                            
                          created_date DATE NOT NULL,
                          FOREIGN KEY (board_idx) REFERENCES board(board_idx),
                          FOREIGN KEY (cate_idx) REFERENCES board(cate_idx),
                          FOREIGN KEY (user_idx) REFERENCES users(user_idx)                                                                                                                                                                     
                          )''')
    # 게시글 참조 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS post_info
                          (info_idx INTEGER PRIMARY KEY NOT NULL,
                           post_idx INTEGER NOT NULL,
                           c_name VARCHAR,
                           c_value VARCHAR,
                           FOREIGN KEY (post_idx) REFERENCES post(post_idx)
                           )''')
    # 게시글 댓글 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS post_comment
                         (cm_idx INTEGER PRIMARY KEY NOT NULL,
                          post_idx INTEGER NOT NULL,
                          user_idx VARCHAR,            
                          cm_content VARCHAR,
                          del_yn VARCHAR(1),
                          created_date DATE NOT NULL,
                          update_date DATE NOT NULL,
                          FOREIGN KEY (post_idx) REFERENCES post(post_idx),
                          FOREIGN KEY (user_idx) REFERENCES users(user_idx)
                          )''')
    # 게시글 대댓글 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS post_replys
                         (rp_idx INTEGER PRIMARY KEY NOT NULL,
                          user_idx VARCHAR NOT NULL,
                          rp_g_idx INTEGER,
                          rp_p_idx INTEGER,
                          rp_depth INTEGER,
                          rp_content VARCHAR,
                          del_yn VARCHAR(1) NOT NULL,
                          created_date DATE NOT NULL,
                          update_date DATE NOT NULL,
                          FOREIGN KEY (rp_p_idx) REFERENCES post_replys(rp_idx),
                          FOREIGN KEY (rp_g_idx) REFERENCES post_comment(cm_idx),
                          FOREIGN KEY (user_idx) REFERENCES users(user_idx)
                         )
                        ''')
    # 게시글 좋아요
    cursor.execute('''CREATE TABLE IF NOT EXISTS post_like
                          (like_idx INTEGER PRIMARY KEY NOT NULL,
                           user_idx INTEGER NOT NULL,
                           post_idx INTEGER NOT NULL,
                           FOREIGN KEY (post_idx) REFERENCES users(user_idx),
                           FOREIGN KEY (post_idx) REFERENCES post(post_idx)
                           )
                           ''')