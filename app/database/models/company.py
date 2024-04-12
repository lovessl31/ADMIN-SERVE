def c_com_tbs(cursor):
    # 회사등록 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS company
                         (com_idx INTEGER PRIMARY KEY,                                                    
                          owner_name VARCHAR,           
                          c_name VARCHAR,
                          c_id VARCHAR NOT NULL UNIQUE                                                                                   
                         )''')
    # 회사 참조 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS company_info
                         (info_idx INTEGER PRIMARY KEY,
                          com_idx INTEGER NOT NULL,                                                                        
                          c_name VARCHAR,
                          c_value VARCHAR,
                          FOREIGN KEY (com_idx) REFERENCES company(com_idx)                                                              
                         )''')