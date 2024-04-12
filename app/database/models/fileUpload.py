def c_file_tbs(cursor):
    # 파일 업로드 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_upload
                         (file_idx INTEGER PRIMARY KEY NOT NULL,                                                                                                               
                          o_file_name VARCHAR(50) NOT NULL,
                          s_file_name VARCHAR(50) NOT NULL,
                          file_size INTEGER NOT NULL,
                          file_type VARCHAR(50) NOT NULL,
                          file_ext VARCHAR(50) NOT NULL,
                          file_path VARCHAR(1000) NOT NULL,
                          domain VARCHAR(100) NOT NULL
                         )''')
    # 회사 사업자등록 파일 저장
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_file
                         (idx INTEGER PRIMARY KEY,
                          com_idx INTEGER NOT NULL,
                          file_idx INTEGER NOT NULL,                                                                                                               
                          FOREIGN KEY (file_idx) REFERENCES file_upload(file_idx),
                          FOREIGN KEY (com_idx) REFERENCES company(com_idx)
                         )''')
    # 게시글 파일 저장
    cursor.execute('''CREATE TABLE IF NOT EXISTS post_file
                          (idx INTEGER PRIMARY KEY,
                           post_idx INTEGER NOT NULL,
                           file_idx INTEGER NOT NULL,                                                                                                               
                           FOREIGN KEY (file_idx) REFERENCES file_upload(file_idx),
                           FOREIGN KEY (post_idx) REFERENCES post(post_idx)
                          )''')