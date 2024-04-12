import app.database.db_manager as DB
from app.utils import get_db_files
'''
1. 메인db에 회사 list 탐색
2. 반복문을 사용하여 회사리스트에 .db를 붙여서 배열에다 담기


'''

def cmt(cursor):
    # 입력 동작
    # 서브 db 가져오
    s_db_list = get_db_files(DB.SUB_DB_PATH1)
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS user_insert_trigger
    AFTER INSERT ON users
    BEGIN
        -- com_id 값을 가져오기 위한 SQL 쿼리
        DECLARE com_idx_value INTEGER;
        SELECT com_id INTO com_id_value FROM company_info WHERE company_name = NEW.company_name;

        -- com_id 값에 따라 다른 하위 데이터베이스에 삽입
        CASE com_id_value
            WHEN 1 THEN
                INSERT INTO sub_db1.sub_users (id, username, email) VALUES (NEW.id, NEW.username, NEW.email);
            WHEN 2 THEN
                INSERT INTO sub_db2.sub_users (id, username, email) VALUES (NEW.id, NEW.username, NEW.email);
            ELSE
                -- 어떤 조건에도 해당하지 않는 경우에 대한 동작
                -- 기본적으로 어느 하위 데이터베이스에도 삽입하지 않음
        END CASE;
    END;
    ''')
