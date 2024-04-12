def c_cate_tbs(cursor):
    # 카테고리
    cursor.execute('''CREATE TABLE IF NOT EXISTS category
                          (cate_idx INTEGER PRIMARY KEY NOT NULL,                        
                           p_cate_idx VARCHAR,
                           cate_name VARCHAR NOT NULL,
                           cate_type VARCHAR NOT NULL,
                           role VARCHAR NOT NULL,
                           cate_vis VARCHAR(1) NOT NULL,
                           LikeSet VARCHAR(1) NOT NULL,                                         
                           FOREIGN KEY (p_cate_idx) REFERENCES Category(cate_idx)                                                                                             
                          )''')

    # 게시판, 카테고리 참조 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS CategoryToBoard
                          (idx INTEGER PRIMARY KEY,
                           cate_idx INTEGER ,
                           board_idx INTEGER ,
                           FOREIGN KEY (board_idx) REFERENCES board(board_idx),
                           FOREIGN KEY (cate_idx) REFERENCES Category(cate_idx)                                                                                     
                          )''')

    # 1차 카테고리 말머리 테이블
    cursor.execute('''CREATE TABLE c_tag (
                        idx INTEGER PRIMARY KEY,
                        cate_idx INTEGER,
                        tag_name VARCHAR(100),
                        FOREIGN KEY (cate_idx) REFERENCES category(cate_idx),
                        CONSTRAINT unique_tag_per_category UNIQUE (cate_idx, tag_name)
                      )''')

